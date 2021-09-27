def handler(doc):
    from quart import Blueprint, request
    from quart.json import jsonify

    swagger_blueprint = Blueprint(
        'swagger_blueprint',
        __name__,
        url_prefix=doc.url_prefix,
        static_url_path=doc.static_uri_relative,
        static_folder=doc.static_dir,
        root_path=doc.static_dir
    )

    @swagger_blueprint.route(
        doc.root_uri_relative(slashes=True), methods=['GET'])
    async def swagger_blueprint_doc_handler():
        return doc.doc_html

    if doc.editor:
        @swagger_blueprint.route(
            doc.editor_uri_relative(slashes=True), methods=['GET'])
        async def swagger_blueprint_editor_handler():
            return doc.editor_html

    @swagger_blueprint.route(doc.swagger_json_uri_relative, methods=['GET'])
    async def swagger_blueprint_config_handler():
        return jsonify(doc.get_config(request.host))

    doc.app.register_blueprint(
        blueprint=swagger_blueprint, url_prefix=doc.url_prefix)


def match(doc):
    try:
        import quart
        if isinstance(doc.app, quart.Quart):
            return handler
    except ImportError:
        pass
    return None
