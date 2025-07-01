import re
import subprocess
from pathlib import Path

from setuptools import find_packages
from setuptools import setup


def get_version():
    version = subprocess.check_output(
        ["git", "describe", "--tags", "--always"]).decode("utf-8").strip()
    if version.startswith("v"):
        version = version[1:]
    version = re.sub(r"-[0-9]+-g", "+", version)
    print(version)
    return version


setup(
    name='swagger-ui-py',
    version=get_version(),
    python_requires='>=3.0.0',
    description=(
        'Swagger UI for Python web framework, '
        'such as Tornado, Flask, Quart, Sanic and Falcon.'
    ),
    long_description=Path(__file__).parent.joinpath('README.md').read_text(),
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    packages=find_packages(),
    package_data={
        'swagger_ui': ['static/*', 'templates/*'],
    },
    install_requires=[
        "jinja2>=2.0",
        "packaging>=20.0",
        "PyYaml>=5.0",
    ],
    url='https://github.com/PWZER/swagger-ui-py',
    author='PWZER',
    author_email='pwzergo@gmail.com',
)
