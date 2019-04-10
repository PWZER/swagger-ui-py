import os

from sanic import Sanic, response

app = Sanic(__name__)


@app.get(r'/hello/world')
async def index_handler(request):
    return response.text('Hello World!!!')


if __name__ == '__main__':
    working_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(working_dir, 'conf/test.yaml')

    from swagger_ui import api_doc
    api_doc(app, config_path=config_path)

    app.run(host='0.0.0.0', port=8989)
