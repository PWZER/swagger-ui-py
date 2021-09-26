def handler(doc):
    from flask import request, jsonify
    from flask.blueprints import Blueprint

    swagger_blueprint = Blueprint(
        'swagger_blueprint', __name__, url_prefix=doc.url_prefix,
        static_folder=doc.static_dir, static_url_path='/'
    )

    @swagger_blueprint.route(r'')
    def swagger_blueprint_doc_handler():
        return doc.doc_html

    @swagger_blueprint.route(r'/')
    def swagger_blueprint_doc_v2_handler():
        return doc.doc_html

    @swagger_blueprint.route(r'/swagger.json')
    def swagger_blueprint_config_handler():
        return jsonify(doc.get_config(request.host))

    if doc.editor:
        @swagger_blueprint.route(r'/editor')
        def swagger_blueprint_editor_handler():
            return doc.editor_html

    doc.app.register_blueprint(swagger_blueprint)


def match(doc):
    try:
        import flask
        if isinstance(doc.app, flask.Flask):
            return handler
    except ImportError:
        pass
    return None
