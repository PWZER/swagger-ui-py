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
    resp = requests.get(
        f'https://api.github.com/repos/{repo}/releases/latest', timeout=120
    )
    latest = json.loads(resp.text)
    tag = latest['tag_name']
    print(f'{repo} latest version is {tag}')
    return tag


def dist_copy(repo, dist_dir):
    # index.html for swagger editor
    if repo == SWAGGER_UI_REPO:
        index_html_path = dist_dir.joinpath('index.html')
        dst_path = templates_dir.joinpath('doc.html')

        # license file
        license_path = dist_dir.parent.joinpath('LICENSE')
        dst_license_path = static_dir.joinpath('LICENSE')
        if license_path.exists():
            shutil.copyfile(license_path, dst_license_path)
        print(f'copy {license_path} => {dst_license_path}')
    elif repo == SWAGGER_EDITOR_REPO:
        index_html_path = dist_dir.parent.joinpath('index.html')
        dst_path = templates_dir.joinpath('editor.html')

    shutil.copyfile(index_html_path, dst_path)
    print(f'copy {index_html_path} => {dst_path}')

    for path in dist_dir.glob('**/*'):
        if path.name == 'index.html':
            continue
        dst_path = static_dir.joinpath(path.relative_to(dist_dir))
        shutil.copyfile(path, dst_path)
        print(f'copy {path} => {dst_path}')


def download_archive(repo, version):
    if version is None:
        version = detect_latest_release(repo)

    file_name = f'{version}.tar.gz'
    save_path = cur_dir.joinpath(file_name)

    if not (cmd_args.no_clean and save_path.exists()):
        archive_url = f'https://github.com/{repo}/archive/{file_name}'
        print(f'archive downloading: {archive_url}')
        with requests.get(archive_url, stream=True) as resp:
            assert resp.status_code == 200, resp.status_code
            with save_path.open('wb') as out:
                shutil.copyfileobj(resp.raw, out)
        print(f'archive download completed: {save_path}')

    print(f'open tarfile: {file_name}')
    tar_file = tarfile.open(save_path)
    tar_file.extractall(path=cur_dir)
    swagger_ui_dir = cur_dir.joinpath(tar_file.getnames()[0])

    dist_copy(repo, swagger_ui_dir.joinpath('dist'))

    if not cmd_args.no_clean:
        print(f'remove {swagger_ui_dir}')
        shutil.rmtree(swagger_ui_dir)

        print(f'remove {save_path}')
        save_path.unlink()

    print('Successed')
    return version


def replace_html_content():
    for html_path in templates_dir.glob('**/*.html'):
        print(html_path)
        with html_path.open('r') as html_file:
            html = html_file.read()

        html = re.sub(r'<title>.*</title>', '<title> {{ title }} </title>', html)
        html = re.sub(r'src="(\./dist/|\./|(?!{{))', 'src="{{ url_prefix }}/static/', html)
        html = re.sub(r'href="(\./dist/|\./|(?!{{))', 'href="{{ url_prefix }}/static/', html)
        html = re.sub(r'https://petstore.swagger.io/v[1-9]/swagger.json', '{{ config_url }}', html)

        if str(html_path).endswith('doc.html'):
            html = re.sub(r'window.onload = function\(\) {.*};$', DOC_HTML_JAVASCRIPT, html,
                          flags=re.MULTILINE | re.DOTALL)
            html = re.sub(
                r'<script .*/swagger-initializer.js".*</script>',
                f'<script>\n{DOC_HTML_JAVASCRIPT}\n</script>',
                html,
            )

        with html_path.open('w') as html_file:
            html_file.write(html)


def replace_readme(ui_version, editor_version):
    readme_path = cur_dir.parent.joinpath('README.md')
    readme = readme_path.read_text(encoding='utf-8')
    if ui_version:
        readme = re.sub(
            r'Swagger UI version is `.*`',
            f'Swagger UI version is `{ui_version}`',
            readme,
        )
        print(f'update swagger ui version: {ui_version}')
    if editor_version:
        readme = re.sub(
            r'Swagger Editor version is `.*`',
            f'Swagger Editor version is `{editor_version}`',
            readme,
        )
        print(f'update swagger editor version: {editor_version}')
    readme_path.write_text(readme)


if __name__ == '__main__':
    cur_dir = Path(__file__).resolve().parent

    static_dir = cur_dir.parent.joinpath('swagger_ui/static')
    if static_dir.exists():
        shutil.rmtree(static_dir)
    static_dir.mkdir(parents=True, exist_ok=True)

    templates_dir = cur_dir.parent.joinpath('swagger_ui/templates')
    if templates_dir.exists():
        shutil.rmtree(templates_dir)
    templates_dir.mkdir(parents=True, exist_ok=True)

    ui_version = editor_version = None

    if cmd_args.ui:
        ui_version = download_archive(SWAGGER_UI_REPO, cmd_args.ui_version)
        replace_html_content()

    if cmd_args.editor:
        editor_version = download_archive(SWAGGER_EDITOR_REPO, cmd_args.editor_version)
        replace_html_content()
    replace_readme(ui_version, editor_version)
