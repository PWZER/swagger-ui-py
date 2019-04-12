# swagger-ui-py
Swagger UI for Python web framework, such Tornado, Flask, Quart, aiohttp and Sanic.

## Usage

- Install

  ```bash
  pip install swagger-ui-py
  ```

- Code

  Using the local config file

  ```python
  from swagger_ui import api_doc
  api_doc(app, config_path='./config/test.yaml', url_prefix='/api/doc', title='API doc')
  ```

  Using config url, but need to suport [CORS](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing)

  ```python
  api_doc(app, config_url='https://petstore.swagger.io/v2/swagger.json', url_prefix='/api/doc', title='API doc')
  ```

  and keep the old way

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
  ```

- Edit `Swagger` config file (JSON or YAML)
  
  Please see [https://swagger.io/resources/open-api/](https://swagger.io/resources/open-api/).

  Enable editor mode

  ```python
  api_doc(app, config_path='./config/test.yaml', editor=True)
  ```

- Access

  Open `http://<host>:<port>/api/doc/editor`, you can edit api doc config file.

  Open `http://<host>:<port>/api/doc` view api doc.

## Swagger UI
Swagger UI version is `3.22.0`. see [https://github.com/swagger-api/swagger-ui](https://github.com/swagger-api/swagger-ui).

You can update Swagger UI version with

```bash
cd swagger-ui-py/tools
python update_swagger_ui.py
```
