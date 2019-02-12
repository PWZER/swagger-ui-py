import os
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape

cur_dir = os.path.dirname(os.path.abspath(__file__))


def get_static_dir():
    return os.path.join(cur_dir, 'static')


def render_html(url_prefix, title):
    env = Environment(loader=FileSystemLoader(os.path.join(cur_dir, 'templates')),
                      autoescape=select_autoescape(['html']))
    template = env.get_template('index.html')
    return template.render(url_prefix=url_prefix, title=title)


def load_swagger_config(config_path, host):
    assert os.path.isfile(config_path), 'config file not exist: %s' % config_path
    with open(config_path, 'r') as config_file:
        if config_path.endswith('.json'):
            config = json.load(config_file)
        elif config_path.endswith('.yaml') or config_file.endswith('.yml'):
            import yaml
            config = yaml.load(config_file)
        else:
            raise Exception('Invalid swagger config file format!!')
        config['host'] = host
    return json.dumps(config, indent=4)
