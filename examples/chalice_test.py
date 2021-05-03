import os

from chalice import Chalice

app = Chalice(app_name="helloworld")

@app.route(r'/hello/world')
def index():
    return {"hello": "world"}

if __name__ == '__main__':
    working_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(working_dir, 'conf/test.yaml')

    from swagger_ui import api_doc
    api_doc(app, config_path=config_path)
