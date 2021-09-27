import json
import yaml
from pathlib import Path


SWAGGER_UI_PY_ROOT = Path(__file__).resolve().parent


def _load_config(content):
    try:
        return json.loads(content)
    except ValueError:
        pass

    try:
        return yaml.load(content, Loader=yaml.FullLoader)
    except yaml.YAMLError:
        pass

    raise Exception('Invalid swagger config format!')
