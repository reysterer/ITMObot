import json
import os

def load_programs(data_dir: str):
    programs = {}
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            with open(os.path.join(data_dir, filename), "r", encoding="utf-8") as f:
                prog = json.load(f)
                programs[prog["program"]] = prog
    return programs