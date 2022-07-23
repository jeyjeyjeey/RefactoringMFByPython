from os import environ, path
import json


def get_data_from_json(entity_name: str) -> dict:
    json_data_dir_path = environ["JSON_DATA_DIR"]
    with open(path.join(json_data_dir_path, f"{entity_name}.json")) as f:
        jd = json.load(f)
    return jd
