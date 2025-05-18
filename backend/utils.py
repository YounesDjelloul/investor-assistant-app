import json
import os

company_data_directory = 'company_data'
PROJECT_DIR = os.path.join(os.path.dirname(__file__), company_data_directory)
AVAILABLE_FILES = {f.replace(".json", ""): f for f in os.listdir(PROJECT_DIR) if f.endswith(".json")}


def load_context_files(filenames: list[str]) -> dict:
    data = {}
    for name in filenames:
        name_key = name.replace(".json", "")
        if name_key in AVAILABLE_FILES:
            path = os.path.join(PROJECT_DIR, AVAILABLE_FILES[name_key])
            with open(path, "r", encoding="utf-8") as f:
                data[name_key] = json.load(f)
    return data


def load_main_context_file() -> dict:
    MAIN_CONTEXT_FILE = "context.json"
    path = os.path.join(PROJECT_DIR, MAIN_CONTEXT_FILE)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
