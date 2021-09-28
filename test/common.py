from pathlib import Path


cur_dir = Path(__file__).resolve().parent

config_path = str(cur_dir.joinpath('conf/test3.yaml'))

mode_list = ['auto', None]

kwargs_list = [
    {
        'url_prefix': '/api/doc',
        'config_path': config_path,
    },
    {
        'url_prefix': '/',
        'config_path': config_path,
    },
    {
        'url_prefix': '',
        'config_path': config_path,
    },
]
