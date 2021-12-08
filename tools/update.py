#! env python
import argparse
import json
import re
import shutil
import tarfile
from pathlib import Path

import requests

parser = argparse.ArgumentParser()
parser.add_argument('--ui', action='store_true',
                    help='Enabled to update swagger ui.')
parser.add_argument('--editor', action='store_true',
                    help='Enabled to update swagger editor.')
parser.add_argument('--ui-version', type=str, default=None,
                    help='Specify the version of swagger ui, Default latest version.')
parser.add_argument('--editor-version', type=str, default=None,
                    help='Specify the version of swagger editor, Default latest version.')
parser.add_argument('--no-clean', action='store_true',
                    help='disable auto clean the temporary files.')
cmd_args = parser.parse_args()


SWAGGER_UI_REPO = 'swagger-api/swagger-ui'
SWAGGER_EDITOR_REPO = 'swagger-api/swagger-editor'


DOC_HTML_JAVASCRIPT = '''window.onload = function() {
    const ui = SwaggerUIBundle({
        {%- for key, value in parameters.items() %}
        {{ key|safe }}: {{ value|safe }},
        {%- endfor %}
    });

    {% if oauth2_config %}
    ui.initOAuth({
        {%- for key, value in oauth2_config.items() %}
        {{ key|safe }}: {{ value|safe }},
        {%- endfor %}
    });
    {% endif %}

    window.ui = ui;
};'''


def detect_latest_release(repo):
    print('detect latest release')
    resp = requests.get('https://api.github.com/repos/{}/releases/latest'.format(repo), timeout=120)
    latest = json.loads(resp.text)
    tag = latest['tag_name']
    print('{} latest version is {}'.format(repo, tag))
    return tag


def dist_copy(repo, dist_dir):
    # index.html for swagger editor
    if repo == SWAGGER_UI_REPO:
        index_html_path = dist_dir.joinpath('index.html')
        dst_path = templates_dir.joinpath('doc.html')
    elif repo == SWAGGER_EDITOR_REPO:
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

    if not (cmd_args.no_clean and save_path.exists()):
        archive_url = 'https://github.com/{}/archive/{}'.format(repo, file_name)
        print('archive downloading: {}'.format(archive_url))
        with requests.get(archive_url, stream=True) as resp:
            assert resp.status_code == 200, resp.status_code
            with save_path.open('wb') as out:
                shutil.copyfileobj(resp.raw, out)
        print('archive download completed: {}'.format(save_path))

    print('open tarfile: {}'.format(file_name))
    tar_file = tarfile.open(save_path)
    tar_file.extractall(path=cur_dir)
    swagger_ui_dir = cur_dir.joinpath(tar_file.getnames()[0])

    dist_copy(repo, swagger_ui_dir.joinpath('dist'))

    if not cmd_args.no_clean:
        print('remove {}'.format(swagger_ui_dir))
        shutil.rmtree(swagger_ui_dir)

        print('remove {}'.format(save_path))
        save_path.unlink()

    print('Successed')


def replace_html_content():
    for html_path in templates_dir.glob('**/*.html'):
        with html_path.open('r') as html_file:
            html_content = html_file.read()

        html_content = re.sub(r'<title>.*</title>', '<title> {{ title }} </title>', html_content)
        html_content = re.sub(r'src="\.(/dist)', 'src="{{ url_prefix }}/static', html_content)
        html_content = re.sub(r'href="\.(/dist)', 'href="{{ url_prefix }}/static', html_content)
        html_content = re.sub(r'src="\.', 'src="{{ url_prefix }}/static', html_content)
        html_content = re.sub(r'href="\.', 'href="{{ url_prefix }}/static', html_content)
        html_content = re.sub(r'https://petstore.swagger.io/v[1-9]/swagger.json',
                              '{{ config_url }}', html_content)

        if str(html_path).endswith('doc.html'):
            html_content = re.sub(r'https://petstore.swagger.io/v[1-9]/swagger.json',
                                  '{{ config_url }}', html_content)
            html_content = re.sub(r'window.onload = function\(\) {.*};$', DOC_HTML_JAVASCRIPT,
                                  html_content, flags=re.MULTILINE | re.DOTALL)

        with html_path.open('w') as html_file:
            html_file.write(html_content)


if __name__ == '__main__':
    cur_dir = Path(__file__).resolve().parent
    static_dir = cur_dir.parent.joinpath('swagger_ui/static')
    templates_dir = cur_dir.parent.joinpath('swagger_ui/templates')

    if cmd_args.ui:
        download_archive(SWAGGER_UI_REPO, cmd_args.ui_version)
        replace_html_content()

    if cmd_args.editor:
        download_archive(SWAGGER_EDITOR_REPO, cmd_args.editor_version)
        replace_html_content()
