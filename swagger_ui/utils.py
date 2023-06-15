import contextlib
import json
from pathlib import Path

import yaml

SWAGGER_UI_PY_ROOT = Path(__file__).resolve().parent


def _load_config(content):
    with contextlib.suppress(ValueError):
        return json.loads(content)
    with contextlib.suppress(yaml.YAMLError):
        return yaml.load(content, Loader=yaml.FullLoader)
    raise ValueError('Invalid swagger config format!')
