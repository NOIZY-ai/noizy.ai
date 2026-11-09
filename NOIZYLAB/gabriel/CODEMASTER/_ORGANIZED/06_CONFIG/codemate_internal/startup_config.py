from BASE.utils.path_selector import PathSelector
from logger.log import logger
from migration import run_migration_steps
import json
import requests
from constants import auth


@logger.catch()
async def perform_basic_startup_configuration() -> bool:
    """Perform basic startup configuration without migration."""
    codemate_folder = PathSelector.get_base_path()
    if not codemate_folder.exists():
        logger.error(f".codemate folder does not exist at {codemate_folder}")
        return False

    path_config_file = codemate_folder / "file_path.json"

    # Create basic config file if it doesn't exist
    if not path_config_file.exists():
        try:
            with open(path_config_file, "w") as f:
                json.dump({"monitored_paths": []}, f, indent=2)
            logger.info(f"Created basic file path config at {path_config_file}")
        except Exception as e:
            logger.error(f"Failed to create basic config file: {e}")
            return False

    return True


@logger.catch()
async def perform_startup_configuration() -> bool:
    codemate_folder = PathSelector.get_base_path()
    if not codemate_folder.exists():
        logger.error(f".codemate folder does not exist at {codemate_folder}")
        return False

    path_config_file = codemate_folder / "file_path.json"
    marker_file = codemate_folder / "migration_marker"

    if marker_file.exists():
        logger.info("Migration marker exists, skipping migration steps")
        return True

    # Run all steps if marker does not exist
    success = await run_migration_steps(codemate_folder, path_config_file)
    if success:
        try:
            marker_file.touch(exist_ok=True)
            logger.info(f"Created migration marker at {marker_file}")
        except Exception as e:
            logger.error(f"Failed to create migration marker: {e}")
            return False

    return success


@logger.catch()
def delete_kb_path(kb_path: str) -> bool:
    """Delete a path from monitored_paths in file_path.json"""
    codemate_folder = PathSelector.get_base_path()
    config_path = codemate_folder / "file_path.json"

    logger.info(f"Deleting path: {kb_path}")

    if not codemate_folder.exists():
        logger.error(f"Base folder does not exist: {codemate_folder}")
        return False

    if not config_path.exists():
        logger.error(f"Config file does not exist: {config_path}")
        return False

    try:
        with open(config_path, "r") as f:
            config = json.load(f)

        monitored_paths = config.get("monitored_paths")
        if not isinstance(monitored_paths, list):
            logger.error("Invalid structure: 'monitored_paths' should be a list.")
            return False

        for path in monitored_paths:
            if path == kb_path:
                monitored_paths.remove(path)
                break

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Failed to update file: {e}")
        return False


def add_file_path(file_path: str) -> bool:
    """Add a path to monitored_paths in file_path.json"""
    codemate_folder = PathSelector.get_base_path()
    config_path = codemate_folder / "file_path.json"

    if not codemate_folder.exists():
        logger.error(f"Base folder does not exist: {codemate_folder}")
        return False

    if not config_path.exists():
        # make file
        with open(config_path, "w") as f:
            json.dump({"monitored_paths": []}, f, indent=2)

    try:
        with open(config_path, "r") as f:
            config = json.load(f)

        monitored_paths = config.get("monitored_paths")
        if not isinstance(monitored_paths, list):
            logger.error("Invalid structure: 'monitored_paths' should be a list.")
            return False

        for file in monitored_paths:
            if file == file_path:
                logger.warning(f"Path already exists in monitored_paths: {file_path}")
                return False

        monitored_paths.append(file_path)

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        logger.info(f"Added path: {file_path}")
        return True

    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Failed to update file: {e}")
        return False


async def save_session(session_id: str) -> bool:
    """Save session id to session.txt, overwriting any existing session"""
    codemate_folder = PathSelector.get_base_path()
    config_path = codemate_folder / "session.txt"

    if not codemate_folder.exists():
        logger.error(f"Base folder does not exist: {codemate_folder}")
        return False

    try:
        # Open in write mode ('w') which automatically overwrites existing content
        with open(config_path, "w") as f:
            f.write(session_id)
        logger.info(f"Session {session_id} saved successfully")
    except OSError as e:
        logger.error(f"Failed to save session: {e}")
        return False
    return True


async def read_session() -> str:
    """Read session id from session.txt"""
    print(f"inside read session ")
    codemate_folder = PathSelector.get_base_path()
    config_path = codemate_folder / "session.txt"

    if not codemate_folder.exists():
        logger.error(f"Base folder does not exist: {codemate_folder}")
        return ""

    if not config_path.exists():
        logger.error(f"Session file does not exist: {config_path}")
        return ""

    try:
        with open(config_path, "r") as f:
            session_id = f.read()
            print(f"session value is : {session_id}")
        return session_id
    except OSError as e:
        logger.error(f"Failed to read session: {e}")
        return ""


async def delete_session() -> bool:
    """Delete session id from session.txt"""
    codemate_folder = PathSelector.get_base_path()
    config_path = codemate_folder / "session.txt"

    if not codemate_folder.exists():
        logger.error(f"Base folder does not exist: {codemate_folder}")
        return False

    if not config_path.exists():
        logger.error(f"Session file does not exist: {config_path}")
        return False

    logger.info(f"Deleting session: {config_path}")

    try:
        config_path.unlink()
        logger.info(f"Session deleted successfully: {config_path}")
        return True
    except OSError as e:
        logger.error(f"Failed to delete session: {e}")
        return False


@logger.catch()
def save_meta_info(data: dict) -> bool:
    """Save meta info to meta_info.json"""
    codemate_folder = PathSelector.get_base_path()
    config_path = codemate_folder / "meta_info.json"

    if not codemate_folder.exists():
        logger.error(f"Base folder does not exist: {codemate_folder}")
        return False

    # if not exists make it file
    if not config_path.exists():
        with open(config_path, "w") as f:
            json.dump({}, f, indent=2)

    try:
        with open(config_path, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Failed to save meta info: {e}")
        return False


@logger.catch()
async def session_refresh(session_id: str):
    """Refresh session id from session.txt"""
    try:
        response = requests.post(
            f"{auth}/session/refresh",
            json={},
            headers={"Content-Type": "application/json", "x-session": session_id},
        )
        if response.status_code == 200:
            result = response.json()
            await save_session(session_id=result.get("session_token"))
            return result.get("session_token")
        else:
            raise Exception(f"Error refreshing session: {response.status_code}")
    except Exception as e:
        logger.error(f"Error refreshing session: {e}")
        raise


@logger.catch()
async def geteco_mode_model():
    stats = {
        "ollama": False,
        "model": False,
        "mini_coder": "",
        "coder": "",
    }

    import requests

    print("[DEBUG] Starting geteco_mode_model...")

    # Check if Ollama server is up
    try:
        print("[DEBUG] Checking if Ollama server is running...")
        response = requests.get("http://localhost:11434", timeout=5000)
        print(f"[DEBUG] Ollama server status: {response.status_code}")
        if response.status_code == 200:
            stats["ollama"] = True
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Ollama is not running: {e}")
        return stats  # Return early if Ollama is unreachable

    # Check available models
    try:
        print("[DEBUG] Fetching available models from Ollama...")
        response = requests.get("http://localhost:11434/v1/models", timeout=5000)
        print(f"[DEBUG] Models endpoint status: {response.status_code}")
        if response.status_code == 200:
            response_json = response.json()
            print(f"[DEBUG] Response JSON: {response_json}")
            data = response_json.get("data", []) or []
            print(f"[DEBUG] Models found: {len(data)}")
            for d in data:
                model_id = d.get("id", "")
                print(f"[DEBUG] Checking model: {model_id}")
                if model_id == "codemate-ai/mini-coder:latest":
                    stats["model"] = True
                    stats["mini_coder"] = "ollama/" + model_id
                    print("[DEBUG] Found mini_coder model")
                elif model_id == "codemate-ai/coder:latest":
                    stats["model"] = True
                    stats["coder"] = "ollama/" + model_id
                    print("[DEBUG] Found coder model")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch models: {e}")

    print(f"[DEBUG] Final stats return: {stats}")
    return stats


@logger.catch()
def get_old_knowledgebases() -> dict:
    """Get old knowledge bases data from state.json if it exists."""
    try:
        base_path = PathSelector.get_base_path()
        input_file = base_path / "state.json"

        if not input_file.exists():
            return {}

        with open(input_file, "r", encoding="utf-8") as f:
            old_data = json.load(f)

        return (
            old_data.get("1.2", {}).get("knowledgebase", {}).get("knowledgebases", {})
        )
    except Exception as e:
        logger.error(f"Failed to get old knowledge bases: {e}")
        return {}


@logger.catch()
async def perform_full_migration_after_qdrant() -> bool:
    """Perform full migration after Qdrant is installed and started."""
    codemate_folder = PathSelector.get_base_path()
    if not codemate_folder.exists():
        logger.error(f".codemate folder does not exist at {codemate_folder}")
        return False

    path_config_file = codemate_folder / "file_path.json"
    marker_file = codemate_folder / "migration_marker"

    if marker_file.exists():
        logger.info("Migration marker exists, skipping migration steps")
        return True

    # Run full migration steps (including Qdrant migration)
    success = await run_migration_steps(codemate_folder, path_config_file)
    if success:
        try:
            marker_file.touch(exist_ok=True)
            logger.info(f"Created migration marker at {marker_file}")
        except Exception as e:
            logger.error(f"Failed to create migration marker: {e}")
            return False

    return success
