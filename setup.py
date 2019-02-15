import os
import sys
from setuptools import setup, find_packages


def load_package_data():
    package_data = []
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    for data_dir in ['static', 'templates']:
        for file_name in os.listdir(os.path.join(cur_dir, 'src/swagger_ui', data_dir)):
            package_data.append(data_dir + '/' + file_name)
    return {'swagger_ui': package_data}


def readme():
    with open('README.md') as f:
        return f.read()


if __name__ == '__main__':
    exclude_packages = []
    if sys.version_info < (3, 0):
        exclude_packages = ['*.py3']

    setup(
        name='swagger-ui-py',
        version='0.1.5',
        description='Swagger UI for Python web framework, such Tornado, Flask, Quart and Sanic.',
        long_description=readme(),
        long_description_content_type='text/markdown',
        license='Apache License 2.0',
        package_dir={'': 'src'},
        include_package_data=True,
        packages=find_packages('src', exclude=exclude_packages),
        package_data=load_package_data(),
        install_requires=['Jinja2>=2.0', 'PyYAML>=2.0'],
        url='https://github.com/PWZER/swagger-ui-py',
        author='PWZER',
        author_email='pwzergo@gmail.com',
    )
