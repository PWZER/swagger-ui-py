import os
from setuptools import setup


def load_data_files():
    data_files = [('python_swagger_ui', ['python_swagger_ui/update-swagger-ui.sh'])]
    cur_dir = os.path.dirname(os.path.abspath(__file__))

    static_dir = 'python_swagger_ui/static'
    static_files = []
    for file_name in os.listdir(os.path.join(cur_dir, static_dir)):
        static_files.append(static_dir + '/' + file_name)
    data_files.append((static_dir, static_files))

    templates_dir = 'python_swagger_ui/templates'
    templates_files = []
    for file_name in os.listdir(os.path.join(cur_dir, templates_dir)):
        templates_files.append(templates_dir + '/' + file_name)
    data_files.append((templates_dir, templates_files))

    return data_files


if __name__ == '__main__':
    setup(
        name='PythonSwaggerUi',
        version='0.1.0',
        description='Swagger UI for Python web framework, such Tornado, Flask and Sanic.',
        license='Apache License 2.0',
        packages=['python_swagger_ui'],
        package_data={
            'python_swagger_ui': ['python_swagger_ui', ]
        },
        # include_package_data=True,
        data_files=load_data_files(),
        url='https://github.com/PWZER/python-swagger-ui',
        author='PWZER',
        author_email='pwzergo@gmail.com',
    )
