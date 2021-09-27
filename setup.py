import os
import platform

from setuptools import find_packages, setup
from distutils.version import StrictVersion


DESCRIPTION = 'Swagger UI for Python web framework, such Tornado, Flask, Quart, Sanic and Falcon.'


def load_package_data():
    package_data = []
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    for data_dir in ['static', 'templates']:
        for file_name in os.listdir(os.path.join(cur_dir, 'swagger_ui', data_dir)):
            package_data.append(data_dir + '/' + file_name)
    return {'swagger_ui': package_data}


def readme():
    with open('README.md') as f:
        return f.read()


def load_requirements():
    with open('./requirements.txt') as requirements_file:
        return [r.strip() for r in requirements_file.read().split()]


if __name__ == '__main__':
    if StrictVersion(platform.python_version()) < StrictVersion('3.0.0'):
        raise Exception("`swagger-ui-py` support python version >= 3.0.0 only.")

    setup(
        name='swagger-ui-py',
        version='21.09.27',
        description=DESCRIPTION,
        long_description=readme(),
        long_description_content_type='text/markdown',
        license='Apache License 2.0',
        include_package_data=True,
        packages=find_packages(),
        package_data=load_package_data(),
        install_requires=load_requirements(),
        url='https://github.com/PWZER/swagger-ui-py',
        author='PWZER',
        author_email='pwzergo@gmail.com',
    )
