#! env python
'''
Usage:
    update.py (ui | editor) [--release=<release>]
'''
import json
import re
import shutil
import tarfile
from pathlib import Path

import requests
from docopt import docopt


def detect_latest_release(repo):
    print('detect latest release')
    resp = requests.get('https://api.github.com/repos/{}/releases/latest'.format(repo))
    latest = json.loads(resp.text)
    tag = latest['tag_name']
    print('{} latest version is {}'.format(repo, tag))
    return tag


def dist_copy(dist_dir):
    # index.html for swagger editor
    if cmd_args['ui']:
        index_html_path = dist_dir.joinpath('index.html')
        dst_path = templates_dir.joinpath('doc.html')
    elif cmd_args['editor']:
        index_html_path = dist_dir.parent.joinpath('index.html')
        dst_path = templates_dir.joinpath('editor.html')

    shutil.copyfile(str(index_html_path), str(dst_path))

    for path in dist_dir.glob('**/*'):
        if path.suffix == '.html':
            continue
        shutil.copyfile(str(path), str(path).replace(str(dist_dir), str(static_dir)))


def download_archive(repo, version):
    if version is None:
        version = detect_latest_release(repo)

    file_name = '{}.tar.gz'.format(version)
    save_path = cur_dir.joinpath(file_name)
    archive_url = 'https://github.com/{}/archive/{}'.format(repo, file_name)

    print('archive downloading: {}'.format(archive_url))
    with requests.get(archive_url, stream=True) as resp:
        assert resp.status_code == 200
        with save_path.open('wb') as out:
            shutil.copyfileobj(resp.raw, out)

    print('open tarfile: {}'.format(file_name))
    tar_file = tarfile.open(save_path)
    tar_file.extractall(path=cur_dir)
    swagger_ui_dir = cur_dir.joinpath(tar_file.getnames()[0])

    dist_copy(swagger_ui_dir.joinpath('dist'))

    print('remove {}'.format(swagger_ui_dir))
    shutil.rmtree(swagger_ui_dir)

    print('remove {}'.format(save_path))
    save_path.unlink()


def replace_html_content():
    for html_path in templates_dir.glob('**/*.html'):
        with html_path.open('r') as html_file:
            index_content = html_file.read()

        index_content = re.sub('<title>.*</title>', '<title> {{ title }} </title>', index_content)
        index_content = re.sub('src="\\.(/dist)', 'src="{{ url_prefix }}', index_content)
        index_content = re.sub('href="\\.(/dist)', 'href="{{ url_prefix }}', index_content)
        index_content = re.sub('src="\\.', 'src="{{ url_prefix }}', index_content)
        index_content = re.sub('href="\\.', 'href="{{ url_prefix }}', index_content)
        index_content = re.sub('https://petstore.swagger.io/v[1-9]/swagger.json',
                               '{{ config_url }}', index_content)
        index_content = re.sub('layout: "StandaloneLayout"', 'layout: "StandaloneLayout", <% if config_json != "null" %>...{{ config_json | safe }}<% endif %>', index_content)

        with html_path.open('w') as html_file:
            html_file.write(index_content)


if __name__ == '__main__':
    cmd_args = docopt(__doc__, version='0.1.0')

    cur_dir = Path(__file__).resolve().parent
    static_dir = cur_dir.parent.joinpath('swagger_ui/static')
    templates_dir = cur_dir.parent.joinpath('swagger_ui/templates')

    if cmd_args['ui']:
        repo = 'swagger-api/swagger-ui'

    if cmd_args['editor']:
        repo = 'swagger-api/swagger-editor'

    download_archive(repo, cmd_args['--release'])
    replace_html_content()
