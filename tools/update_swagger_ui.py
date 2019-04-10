#! env python
import json
import os
import re
import shutil
import tarfile

import requests


def detect_swagger_ui_latest_release():
    resp = requests.get('https://api.github.com/repos/swagger-api/swagger-ui/releases/latest')
    latest = json.loads(resp.text)
    return latest['tag_name']


def dist_copy(dist_dir):
    for file_name in os.listdir(dist_dir):
        file_path = os.path.join(dist_dir, file_name)
        if file_name.endswith(('.html', )):
            shutil.copyfile(file_path, os.path.join(templates_dir, file_name))
        else:
            shutil.copyfile(file_path, os.path.join(static_dir, file_name))


def download_archive(version):
    file_name = '{}.tar.gz'.format(version)
    save_path = os.path.join(cur_dir, file_name)
    archive_url = 'https://github.com/swagger-api/swagger-ui/archive/' + file_name
    print('archive downloading: {}'.format(archive_url))
    with requests.get(archive_url, stream=True) as resp:
        assert resp.status_code == 200
        with open(save_path, 'wb') as out:
            shutil.copyfileobj(resp.raw, out)

    tar_file = tarfile.open(save_path)
    tar_file.extractall(path=cur_dir)
    swagger_ui_dir = os.path.join(cur_dir, tar_file.getnames()[0])
    dist_copy(os.path.join(swagger_ui_dir, 'dist'))
    print('remove {}'.format(swagger_ui_dir))
    shutil.rmtree(swagger_ui_dir)
    print('remove {}'.format(save_path))
    os.unlink(save_path)


def replace_index_html():
    index_path = os.path.join(templates_dir, 'index.html')
    with open(index_path, 'r') as index_file:
        index_content = index_file.read()

    index_content = re.sub('<title>.*</title>', '<title> {{ title }} </title>', index_content)
    index_content = re.sub('src="\\.', 'src="{{ url_prefix }}', index_content)
    index_content = re.sub('href="\\.', 'href="{{ url_prefix }}', index_content)
    index_content = re.sub('https://petstore.swagger.io/v[1-9]/swagger.json',
                           '{{ config_url }}', index_content)

    with open(index_path, 'w') as index_file:
        index_file.write(index_content)


def main():
    latest_version = detect_swagger_ui_latest_release()
    print('latest_version: {}'.format(latest_version))
    download_archive(latest_version)
    replace_index_html()


if __name__ == '__main__':
    cur_dir = os.path.dirname(os.path.abspath(__file__))

    static_dir = os.path.join(os.path.dirname(cur_dir), 'swagger_ui/static')
    templates_dir = os.path.join(os.path.dirname(cur_dir), 'swagger_ui/templates')
    main()
