from pathlib import Path

from setuptools import find_packages, setup

setup(
    name='swagger-ui-py',
    version='23.6.15',
    description=(
        'Swagger UI for Python web framework, '
        'such as Tornado, Flask, Quart, Sanic and Falcon.'
    ),
    long_description=Path(__file__).parent.joinpath('README.md').read_text(),
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    python_requires='>=3.0.0',
    packages=find_packages(),
    package_data={
        'swagger_ui': ['static/*', 'templates/*'],
    },
    install_requires=[
        "jinja2>=2.0",
        "PyYaml>=5.0",
    ],
    url='https://github.com/PWZER/swagger-ui-py',
    author='PWZER',
    author_email='pwzergo@gmail.com',
)
