from pathlib import Path
import re
import yaml
import os

env_pattern = re.compile(r'\$\{\{\s*(\w+)\s*\}\}([^:]*)?(:\s*(\w+)\s*)?')

def load_yaml(file_path: Path):
    with open(file_path) as f:
        yml = yaml.safe_load(f)
        result = replace_env_from_yaml(yml)
    return result

def replace_env_from_yaml(item):
    for k, v in item.items():
        if isinstance(v, dict):
            item[k] = replace_env_from_yaml(v)
        if isinstance(v, str):
            matched = env_pattern.match(v)
            if not matched:
                item[k] = v
                continue
            
            grouped = matched.groups()
            if os.environ.get(grouped[0],None):
                item[k] = os.environ.get(grouped[0]) +\
                    (grouped[1] if grouped[1] else '')
            else:
                item[k] = grouped[3]

        if isinstance(v, int):
            item[k] = v

    return item