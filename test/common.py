from itertools import product
from pathlib import Path

cur_dir = Path(__file__).resolve().parent

config_path = str(cur_dir.joinpath('conf/test3.yaml'))
config_content = Path(config_path).read_text()

mode_list = ['auto', None]

kwargs_list = [
    {
        'url_prefix': '/api/doc',
        'config_path': config_path,
    },
    {
        'url_prefix': '/api/doc',
        'config_path': config_path,
        'editor': True,
    },
    {
        'url_prefix': '/',
        'config_path': config_path,
    },
    {
        'url_prefix': '',
        'config_path': config_path,
    },
    {
        'url_prefix': '/',
        'config_path': config_path,
        'config_rel_url': '/swagger.json',
    },
]

parametrize_list = list(product(mode_list, kwargs_list))
