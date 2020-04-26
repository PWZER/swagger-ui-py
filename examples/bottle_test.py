import os
from bottle import Bottle, run

app = Bottle()


@app.route('/hello/world')
def hello():
    return 'Hello World!!!'


if __name__ == '__main__':
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(cur_dir, 'conf/test.yaml')

    from swagger_ui import api_doc
    api_doc(app, config_path=config_path, url_prefix='/api/doc')
    run(app, host='0.0.0.0', port=8989, debug=True)
