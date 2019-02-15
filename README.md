# swagger-ui-py
Swagger UI for Python web framework, such Tornado, Flask, Quart, aiohttp and Sanic.

## Usage

- Install

  ```bash
  pip install swagger-ui-py
  ```

- Code

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

- Access

  `http://<host>:<port>/api/doc`, open the url in your browser.

## Swagger UI
Swagger UI version is `3.19.3`. see [https://github.com/swagger-api/swagger-ui](https://github.com/swagger-api/swagger-ui).
