# import multiprocessing
# import sys
# import os

# # CRITICAL: This must be at the very top after imports for PyInstaller
# if __name__ == '__main__':
#     # This prevents the infinite restart loop in PyInstaller executables
#     multiprocessing.freeze_support()

#     # Set multiprocessing start method for Windows compatibility
#     if sys.platform.startswith('win'):
#         multiprocessing.set_start_method('spawn', force=True)
#
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import socketio
import constants
from BASE.events.kb.upload_kb import handle_upload_event
from BASE.events.kb.cloud_kb_upload import handle_upload_to_cloud_event
from BASE.events.kb.cloud_sync_kb import handle_sync_to_cloud_event
from BASE.events.fs.fs import (
    handle_get_file_paths_recursive_event,
    handle_get_folder_paths_recursive_event,
)

app = FastAPI(title="CodeMate Socket.IO API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    ping_interval=constants.SOCKETIO_PING_INTERVAL,
    ping_timeout=constants.SOCKETIO_PING_TIMEOUT,
    max_http_buffer_size=constants.SOCKETIO_MAX_HTTP_BUFFER_SIZE,
    always_connect=True,  # Allow reconnections
    engineio_logger=False,  # Disable verbose logging
    transports=["websocket", "polling"],  # Allow fallback to polling if websocket fails
)


@sio.event
async def connect(sid, _environ=None):
    """Handle client connection"""
    pass


@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    pass


@sio.on("upload")
async def handle_upload(sid, data):
    """Handle upload events using the refactored upload functionality"""
    await handle_upload_event(sio, sid, data)


@sio.on("upload_to_cloud")
async def handle_upload_to_cloud(sid, data):
    """Handle upload events using the refactored upload functionality"""
    await handle_upload_to_cloud_event(sio, sid, data)


@sio.on("sync_to_cloud")
async def handle_sync_to_cloud(sid, data):
    """Handle upload events using the refactored upload functionality"""
    await handle_sync_to_cloud_event(sio, sid, data)


@sio.on("get_file_paths_recursive")
async def handle_get_file_paths_recursive(sid, data):
    """Handle get_file_paths_recursive event"""
    await handle_get_file_paths_recursive_event(sio, sid, data)


@sio.on("get_folder_paths_recursive")
async def handle_get_folder_paths_recursive(sid, data):
    """Handle get_folder_paths_recursive event"""
    await handle_get_folder_paths_recursive_event(sio, sid, data)


# Mount Socket.IO app
socket_app = socketio.ASGIApp(sio, app)

# Export socket_app as the main app for the combine_servers.py
app = socket_app

# if __name__ == "__main__":
#     uvicorn.run("websocket_server:app", host="127.0.0.1", port=45224, workers=1)
