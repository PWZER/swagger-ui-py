def handler(doc):
    from flask import jsonify
    from flask import request
    from flask.blueprints import Blueprint

    swagger_blueprint = Blueprint(
        doc.blueprint_name,
        __name__,
        url_prefix=doc.url_prefix,
        static_folder=doc.static_dir,
        static_url_path=doc.static_uri_relative,
    )

    @swagger_blueprint.route(doc.root_uri_relative(slashes=True))
    @swagger_blueprint.route(doc.root_uri_relative(slashes=False))
    def swagger_blueprint_doc_handler():
        return doc.doc_html

    if doc.editor:
        @swagger_blueprint.route(doc.editor_uri_relative(slashes=True))
        @swagger_blueprint.route(doc.editor_uri_relative(slashes=False))
        def swagger_blueprint_editor_handler():
            return doc.editor_html

    if doc.config_rel_url is None:
        @swagger_blueprint.route(doc.swagger_json_uri_relative)
        def swagger_blueprint_config_handler():
            return jsonify(doc.get_config(request.host))

    doc.app.register_blueprint(swagger_blueprint)


def match(doc):
    try:
        import flask
        if isinstance(doc.app, flask.Flask):
            return handler
    except ImportError:
        pass
    return None
