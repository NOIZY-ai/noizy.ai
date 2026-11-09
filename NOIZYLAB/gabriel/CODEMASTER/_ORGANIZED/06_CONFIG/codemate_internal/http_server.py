from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

import logging
import time
from datetime import datetime
from BASE.http.chat.chat import chat_stream, __chat_stream
from BASE.http.chat.history import (
    get_all_chat_history,
    get_chat_history,
    delete_chat_history,
)
from BASE.http.watchdog import watchdog_file_delete, watchdog_file_update
from BASE.http.kb.delete_kb import delete_kb_source
from BASE.http.kb.list_kbs import list_knowledge_bases

# from BASE.http.swagger import swagger_list
from BASE.http.auto_actions import auto_actions
import json
from BASE.http.swagger import swagger_stream, swagger_list
from BASE.http.codelens import debug_code, optimize_code, review_code, test_code
from ipc import IPC
from startup_config import save_session, delete_session, save_meta_info
from BASE.http import custom_prompts
import constants
from BASE.http.chat.utils import get_chat_fork
from BASE.http.chat.image import upload_image_to_cloud, get_image_from_cloud
from BASE.actions.context_search import process_new_kb_search

ipc_ = IPC.connect()

# Setup worker request tracking
worker_id = os.getpid()
request_count = 0

# Configure logging for worker tracking
logging.basicConfig(
    level=logging.INFO,
    format=f"[Worker-{worker_id}] %(asctime)s - %(message)s",
    handlers=[logging.FileHandler("logs/worker_requests.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

app = FastAPI(title="CodeMate HTTP API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    global request_count
    request_count += 1

    # Log request queued (arrived and dequeued by worker)
    log_entry_queued = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event": "request_queued",
        "request_id": request_count,
        "method": request.method,
        "url": str(request.url),
        "worker_id": worker_id,
    }
    with open("request-log.json", "a") as f:
        json.dump(log_entry_queued, f)
        f.write("\n")

    start_time = time.time()

    # Log request processing
    log_entry_processing = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event": "request_processing",
        "request_id": request_count,
        "worker_id": worker_id,
    }
    with open("request-log.json", "a") as f:
        json.dump(log_entry_processing, f)
        f.write("\n")

    response = await call_next(request)

    process_time = time.time() - start_time

    # Log request completed
    log_entry_completed = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event": "request_completed",
        "request_id": request_count,
        "status_code": response.status_code,
        "process_time": process_time,
        "worker_id": worker_id,
    }
    with open("request-log.json", "a") as f:
        json.dump(log_entry_completed, f)
        f.write("\n")

    logger.info(
        f"Request #{request_count}: {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s"
    )

    return response


@app.get("/")
async def root():
    time.sleep(0.2)
    return {"message": "Hello World"}


@app.post("/base_url/set")
async def set_baseURL(request: Request):
    data = await request.json()
    ipc_.set("base_url", data.get("url", "codemate.ai"))
    with open("BASE_CONTROL", "w", encoding="utf-8") as e:
        e.write(data.get("url", "codemate.ai"))


@app.post("/chat/stream")
async def chat_stream_handler(request: Request):
    print("Received chat request")
    data = await request.json()

    session_id = ipc_.get("current_session")
    conversation_id = data.get("conversation_id", "")

    return StreamingResponse(
        chat_stream(
            messages=data["messages"],
            call_for="chat",
            session_id=session_id,
            is_web_search=data["web_search"],
            continue_required=data.get("continue_required", False),
            image=data.get("image", False),
            mode=data["mode"].upper(),
            conversation_id=conversation_id,
            provide_followups=data.get("provide_followups", False),
        ),
        media_type="text/event-stream",
    )


# @app.post("/v1/chat/completions")
# async def chat_stream_handler(request: Request):
#     print("Received chat request")
#     data = await request.json()

#     session_id = ipc_.get("current_session")
#     conversation_id = data.get("conversation_id", "")

#     return StreamingResponse(
#         chat_stream(
#             messages=data["messages"],
#             call_for="chat",
#             session_id=session_id,
#             is_web_search=data["web_search"],
#             continue_required=data.get("continue_required", False),
#             image=data.get("image", False),
#             mode=data["mode"].upper(),
#             conversation_id=conversation_id,
#             provide_followups=data.get("provide_followups", False),
#         ),
#         media_type="text/event-stream",
#     )


@app.get("/v1/chat/completions")
@app.post("/v1/chat/completions")
async def handle_chat(request: Request):
    request_body = await request.json()
    mode = request.headers.get("Authorization").split("Bearer ")[1].strip()
    result = await __chat_stream(
        messages=request_body.get("messages", []),
        call_for=request_body.get("call_for", "chat"),
        image=request_body.get("image", False),
        mode=mode,
        model=request_body.get("model", "openai/bodh-x1"),
        tools=request_body.get("tools", []),
    )
    if result["streaming"]:
        # Streaming FTW
        return StreamingResponse(
            result["generator"](),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
            },
        )
    else:
        # Regular JSON response, no drama
        return JSONResponse(content=result["data"])


@app.post("/swagger/stream")
async def swagger_stream_handler(request: Request):
    data = await request.json()

    print(f"swagger data : {json.dumps(data, indent=2)}")

    swagger_data = data

    return StreamingResponse(
        swagger_stream(
            swagger_data,
        ),
        media_type="text/event-stream",
    )


@app.get("/eco")
async def eco_installation():
    stats = {
        "ollama": False,
        "model": False,
        "suggested_model": "codemate-ai/mini-coder:latest",
    }

    try:
        import requests

        response = requests.get("http://localhost:11434")
        if response.status_code == 200:
            stats["ollama"] = True
        response = requests.get("http://localhost:11434/v1/models")
        if response.status_code == 200:
            response = response.json()
            data = response.get("data", []) or []
            for d in data:
                if (
                    d.get("id", "") == "codemate-ai/mini-coder:latest"
                    or d.get("id", "") == "codemate-ai/coder:latest"
                ):
                    stats["model"] = True

        # Get total RAM of the device
        try:
            import psutil

            total_ram = psutil.virtual_memory().total / (1024**3)
            if total_ram >= 18:
                stats["suggested_model"] = "codemate-ai/coder:latest"
            else:
                stats["suggested_model"] = "codemate-ai/mini-coder:latest"
        except:
            stats["suggested_model"] = "codemate-ai/mini-coder:latest"
    except:
        pass

    return JSONResponse(stats)


@app.delete("/chat/history/{conversation_id}")
async def chat_history_delete_handler(request: Request):
    conversation_id = request.path_params["conversation_id"]
    return JSONResponse(await delete_chat_history(conversation_id))


@app.get("/chat/history/{conversation_id}")
async def chat_history_handler(request: Request):
    conversation_id = request.path_params["conversation_id"]
    return JSONResponse(await get_chat_history(conversation_id))


@app.post("/chat/history/all")
async def chat_history_handler(request: Request):
    print("Received all chat history request")
    session_id = ipc_.get("current_session") if ipc_.get("current_session") else None
    print(f"Session ID: {session_id}")
    print(f"Received all chat history request")
    if not session_id:
        return JSONResponse({"status": "error", "message": "No session provided"})

    return JSONResponse(await get_all_chat_history(session_id))


@app.post("/swagger_list")
async def swagger_list_handler(request: Request):
    data = await request.json()
    print(f"swagger list data : {json.dumps(data, indent=2)}")
    return JSONResponse(await swagger_list(data))


@app.post("/delete_kb")
async def delete_kb_handler(request: Request):
    data = await request.json()
    kbid = data["kbid"]
    # source = data["source"]

    if not kbid:
        return JSONResponse(
            {"status": "error", "message": "Knowledge base ID and source is required"}
        )

    return JSONResponse(await delete_kb_source(kbid=kbid))


@app.get("/list_kbs")
async def list_kb(request: Request):
    include_cloud = request.query_params.get("include_cloud", "false").lower() == "true"
    session = ipc_.get("current_session")
    if session is None:
        return JSONResponse({"status": "error", "message": "No session found"})

    print(f"include_cloud: {include_cloud}, session: {session}")

    result = await list_knowledge_bases(include_cloud=include_cloud)
    return JSONResponse(result)


# @app.post("/swagger/list")
# async def get_swagger_list(request: Request):
#     data = await request.json()
#     return JSONResponse(await swagger_list(data))


@app.post("/watchdog/file_delete")
async def watchdog_file_delete_handler(request: Request):
    data = await request.json()
    file_path = data.get("file_path", "")
    if not file_path:
        return JSONResponse({"status": "error", "message": "File path not provided"})

    result = await watchdog_file_delete(file_path=file_path)
    return JSONResponse(result)


@app.post("/watchdog/file_update")
async def watchdog_file_update_handler(request: Request):
    data = await request.json()
    file_path = data.get("file_path", "")
    if not file_path:
        return JSONResponse({"status": "error", "message": "File path not provided"})

    result = await watchdog_file_update(file_path=file_path)
    return JSONResponse(result)


@app.post("/auto-actions/{operation}")
async def auto_actions_handler(request: Request, operation: str):
    data = await request.json()
    session_id = ipc_.get("current_session")
    if session_id is None:
        return JSONResponse({"status": "error", "message": "No session found"})
    result = await auto_actions(data, session_id=session_id, operation=operation)
    return JSONResponse(result)


@app.post("/debug/code")
async def debug_code_handler(request: Request):
    data = await request.json()
    session_id = ipc_.get("current_session")
    if session_id is None:
        return JSONResponse({"status": "error", "message": "No session found"})
    # print(f"Received debug code request: {data}")
    result = await debug_code(data, session_id=session_id)
    return JSONResponse(result)


@app.post("/test/code")
async def test_code_handler(request: Request):
    data = await request.json()
    session_id = ipc_.get("current_session")
    if session_id is None:
        return JSONResponse({"status": "error", "message": "No session found"})
    result = await test_code(data, session_id=session_id)
    return JSONResponse(result)


@app.post("/review/code")
async def review_code_handler(request: Request):
    data = await request.json()
    session_id = ipc_.get("current_session")
    if session_id is None:
        return JSONResponse({"status": "error", "message": "No session found"})
    result = await review_code(data, session_id=session_id)
    return JSONResponse(result)


@app.post("/optimize/code")
async def optimize_code_handler(request: Request):
    data = await request.json()
    session_id = ipc_.get("current_session")
    if session_id is None:
        return JSONResponse({"status": "error", "message": "No session found"})
    result = await optimize_code(data, session_id=session_id)
    return JSONResponse(result)


@app.post("/register_meta")
async def register_meta(request: Request):
    data = await request.json()
    extension_version = data.get("extension_version", "")
    subsystem_version = data.get("subsystem_version", "")
    base_url = data.get("base_url", {})
    general_url = base_url.get("general", "https://backend.v3." + ipc_.get("base_url"))
    chat_url = base_url.get("chat", "https://backend.v3." + ipc_.get("base_url"))
    codebase_url = base_url.get(
        "codebase", "https://codebase.v3." + ipc_.get("base_url")
    )
    autocomplete_url = base_url.get(
        "autocomplete", "https://autocomplete." + ipc_.get("base_url")
    )

    if extension_version or subsystem_version:
        ipc_.set("extension_version", extension_version)
        ipc_.set("subsystem_version", subsystem_version)
        save_meta_info(
            {
                "extension_version": extension_version,
                "subsystem_version": subsystem_version,
                "base_url": base_url,
            }
        )
        return JSONResponse({"status": "success", "message": "Registered successfully"})
    else:
        return JSONResponse(
            {
                "status": "error",
                "message": "No extension version or subsystem version provided",
            }
        )


@app.post("/set_session")
async def set_session(request: Request):
    data = await request.json()
    session_id = data.get("session_id", "")

    if session_id:
        ipc_.set("current_session", session_id)
        await save_session(session_id)
        return JSONResponse(
            {
                "session_id": session_id,
                "status": "success",
                "message": "Session ID set successfully",
            }
        )
    else:
        return JSONResponse(
            {"session_id": "", "status": "error", "message": "No session ID provided"}
        )


@app.get("/get_session")
async def get_session(request: Request):
    try:
        current_session = (
            ipc_.get("current_session") if ipc_.get("current_session") else None
        )
        return JSONResponse(
            {
                "session_id": current_session,
                "status": "success",
                "message": "Session ID retrieved successfully",
            }
        )

    except Exception as e:
        return JSONResponse(
            {
                "session_id": None,
                "status": "error",
                "message": f"Failed to retrieve session: {str(e)}",
            }
        )


@app.post("/logout")
async def logout(request: Request):
    ipc_.set("current_session", None)
    await delete_session()
    return JSONResponse(
        {"status": "logged_out", "message": "Session cleared successfully"}
    )


# CUSTOM PROMPTS
@app.post("/prompts/create")
async def create_prompt(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    name = data.get("name", "")

    response = await custom_prompts.create_prompt(prompt=prompt, name=name)
    return JSONResponse(response)


@app.post("/prompts/edit")
async def edit_prompt(request: Request):
    data = await request.json()
    name = data.get("name", "")
    prompt = data.get("prompt", "")
    prompt_id = data.get("prompt_id", "")

    response = await custom_prompts.edit_prompt(
        prompt=prompt, name=name, prompt_id=prompt_id
    )
    return JSONResponse(response)


@app.post("/prompts/delete")
async def delete_prompt(request: Request):
    data = await request.json()
    prompt_id = data.get("prompt_id")

    response = await custom_prompts.delete_prompt(prompt_id=prompt_id)
    return JSONResponse(response)


@app.post("/prompts/get/all")
async def get_prompts_all():
    response = await custom_prompts.get_prompts_all()
    return JSONResponse(response)


@app.post("/prompts/get/one")
async def get_prompt(request: Request):
    data = await request.json()
    prompt_id = data.get("prompt_id", "")
    response = await custom_prompts.get_prompt(prompt_id=prompt_id)


@app.post("/personality/set")
async def set_personality(request: Request):
    data = await request.json()
    with open(
        os.path.join(constants.HOME_PATH, "personality.txt"), "w+", encoding="utf-8"
    ) as f:
        f.write(data["personality"])
    return JSONResponse(
        {"status": "success", "message": "Personality set successfully"}
    )


@app.post("/personality/get")
async def get_personality(request: Request):
    try:
        with open(
            os.path.join(constants.HOME_PATH, "personality.txt"), "r", encoding="utf-8"
        ) as f:
            personality = f.read()
    except:
        personality = ""
    return JSONResponse({"personality": personality})


@app.post("/personality/toggle")
async def toggle_personality():
    ipc_.set(
        "personality_enabled",
        not ipc_.get("personality_enabled")
        if ipc_.get("personality_enabled")
        else False,
    )
    return JSONResponse(
        {"status": "success", "message": "Personality toggled successfully"}
    )


@app.get("/personality/status")
async def get_personality_status():
    return JSONResponse(
        {
            "status": ipc_.get("personality_enabled")
            if ipc_.get("personality_enabled")
            else False
        }
    )


@app.post("/chat/fork")
async def get_chat_fork_handler(request: Request):
    data = await request.json()

    response = await get_chat_fork(
        chat_id=data.get("chat_id", ""), message_index=data.get("message_index", -1)
    )
    return JSONResponse(response)


@app.post("/upload/image")
async def upload_image(request: Request):
    try:
        data = await request.json()
        image = data.get("image", "")
        if not image:
            return JSONResponse({"status": "error", "message": "No image provided"})

        response = await upload_image_to_cloud(image=image)
        return response
    except Exception as e:
        import traceback

        traceback.print_exc()


@app.post("/uploaded/images/{image_id}")
async def get_uploaded_image(request: Request):
    image_id = request.path_params["image_id"]
    response = await get_image_from_cloud(image_id=image_id)
    return JSONResponse(response)


@app.get("/service/stop")
async def stop_service(request: Request):
    import signal

    pid = ipc_.get("self.pid")
    if pid is None:
        return JSONResponse({"status": "error", "message": "No PID found"})

    try:
        os.kill(pid, signal.SIGTERM)
        return JSONResponse(
            {"status": "success", "message": "Service stopped successfully"}
        )
    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": f"Error stopping service: {e}"}
        )


# if __name__ == "__main__":
#     uvicorn.run("http_server:app", host="127.0.0.1", port=45223, workers=4)


@app.post("/kb_search")
async def kb_search_handler(request: Request):
    data = await request.json()
    query = data["query"]
    kbid = data["kbid"]
    session = ipc_.get("current_session")
    results = await process_new_kb_search(query, kbid, session)
    return JSONResponse(results)
