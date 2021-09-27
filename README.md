# swagger-ui-py
Swagger UI for Python web framework, such Tornado, Flask, Quart, aiohttp, Sanic and Falcon.

Only support Python3.

## Supported

- [Tornado](https://www.tornadoweb.org/en/stable/)
- [Flask](https://flask.palletsprojects.com/)
- [Sanic](https://sanicframework.org/en/)
- [AIOHTTP](https://docs.aiohttp.org/en/stable/)
- [Quart](https://pgjones.gitlab.io/quart/)
- [Starlette](https://www.starlette.io/)
- [Falcon](https://falcon.readthedocs.io/en/stable/)
- [Bottle](https://bottlepy.org/docs/dev/)

## Usage

- Install

  ```bash
  pip3 install swagger-ui-py
  ```

- Code

  Using the local config file

  ```python
  from swagger_ui import api_doc
  api_doc(app, config_path='./config/test.yaml', url_prefix='/api/doc', title='API doc')
  ```

  Or using config url, but need to suport [CORS](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing)

  ```python
  api_doc(app, config_url='https://petstore.swagger.io/v2/swagger.json', url_prefix='/api/doc', title='API doc')
  ```

  Or using the config spec string

  ```python
  from swagger_ui import api_doc
  spec_string = '{"openapi":"3.0.1","info":{"title":"python-swagger-ui test api","description":"python-swagger-ui test api","version":"1.0.0"},"servers":[{"url":"http://127.0.0.1:8989/api"}],"tags":[{"name":"default","description":"default tag"}],"paths":{"/hello/world":{"get":{"tags":["default"],"summary":"output hello world.","responses":{"200":{"description":"OK","content":{"application/text":{"schema":{"type":"object","example":"Hello World!!!"}}}}}}}},"components":{}}'

  api_doc(app, config_spec=spec_string, url_prefix='/api/doc', title='API doc')
  ```

  Or using the config dict

  ```python
  from swagger_ui import api_doc
  config = {"openapi":"3.0.1","info":{"title":"python-swagger-ui test api","description":"python-swagger-ui test api","version":"1.0.0"},"servers":[{"url":"http://127.0.0.1:8989/api"}],"tags":[{"name":"default","description":"default tag"}],"paths":{"/hello/world":{"get":{"tags":["default"],"summary":"output hello world.","responses":{"200":{"description":"OK","content":{"application/text":{"schema":{"type":"object","example":"Hello World!!!"}}}}}}}},"components":{}}

  api_doc(app, config=config, url_prefix='/api/doc', title='API doc')
  ```

  And suport config file with editor

  ```python
  api_doc(app, config_path='./config/test.yaml', editor=True)
  ```

  And keep the old way

  ```python
  # for Tornado
  from swagger_ui import tornado_api_doc
  tornado_api_doc(app, config_path='./conf/test.yaml', url_prefix='/api/doc', title='API doc')

  # for Sanic
  from swagger_ui import sanic_api_doc
  sanic_api_doc(app, config_path='./conf/test.yaml', url_prefix='/api/doc', title='API doc')

  # for Flask
  from swagger_ui import flask_api_doc
  flask_api_doc(app, config_path='./conf/test.yaml', url_prefix='/api/doc', title='API doc')

  # for Quart
  from swagger_ui import quart_api_doc
  quart_api_doc(app, config_path='./conf/test.yaml', url_prefix='/api/doc', title='API doc')

  # for aiohttp
  from swagger_ui import aiohttp_api_doc
  aiohttp_api_doc(app, config_path='./conf/test.yaml', url_prefix='/api/doc', title='API doc')

  # for Falcon
  from swagger_ui import falcon_api_doc
  falcon_api_doc(app, config_path='./conf/test.yaml', url_prefix='/api/doc', title='API doc')
  ```

- Edit `Swagger` config file (JSON or YAML)

  Please see [https://swagger.io/resources/open-api/](https://swagger.io/resources/open-api/).

- Access

  Open `http://<host>:<port>/api/doc/editor`, you can edit api doc config file.

  Open `http://<host>:<port>/api/doc` view api doc.

## Swagger UI
Swagger UI version is `v3.52.3`. see [https://github.com/swagger-api/swagger-ui](https://github.com/swagger-api/swagger-ui).

## Swagger Editor
Swagger Editor version is `v3.18.2`. see [https://github.com/swagger-api/swagger-editor](https://github.com/swagger-api/swagger-editor).

## Update
You can update swagger ui and swagger editor version with

```bash
cd swagger-ui-py/tools

python update.py --ui --editor
```
