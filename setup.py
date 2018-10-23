import os
import sys
from setuptools import setup


def load_data_files():
    data_files = [('swagger_ui', ['swagger_ui/update-swagger-ui.sh'])]
    cur_dir = os.path.dirname(os.path.abspath(__file__))

    static_dir = 'swagger_ui/static'
    static_files = []
    for file_name in os.listdir(os.path.join(cur_dir, static_dir)):
        static_files.append(static_dir + '/' + file_name)
    data_files.append((static_dir, static_files))

    templates_dir = 'swagger_ui/templates'
    templates_files = []
    for file_name in os.listdir(os.path.join(cur_dir, templates_dir)):
        templates_files.append(templates_dir + '/' + file_name)
    data_files.append((templates_dir, templates_files))

    return data_files


def readme():
    with open('README.md') as f:
        return f.read()


if __name__ == '__main__':
    py_modules = [
        'swagger_ui.utils',
        'swagger_ui.flask_swagger_ui',
        'swagger_ui.tornado_swagger_ui',
    ]

    if sys.version_info >= (3, 0):
        py_modules.append('swagger_ui.sanic_swagger_ui')

    setup(
        name='swagger-ui-py',
        version='0.1.0',
        description='Swagger UI for Python web framework, such Tornado, Flask and Sanic.',
        long_description=readme(),
        long_description_content_type='text/markdown',
        license='Apache License 2.0',
        py_modules=py_modules,
        data_files=load_data_files(),
        # include_package_data=False,
        url='https://github.com/PWZER/swagger-ui-py',
        author='PWZER',
        author_email='pwzergo@gmail.com',
    )
