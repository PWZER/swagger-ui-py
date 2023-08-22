def handler(doc):
    from pathlib import Path

    from chalice import Blueprint
    from chalice import NotFoundError
    from chalice import Response

    cur_dir = Path(__file__).resolve().parent
    static_dir = cur_dir.parent.joinpath("static")

    bp = Blueprint(__name__)

    @bp.route(doc.root_uri_relative(slashes=True), methods=["GET"])
    def bp_doc_handler():
        return Response(
            body=doc.doc_html,
            status_code=200,
            headers={"Content-Type": "text/html"},
        )

    if doc.config_rel_url is None:
        @bp.route(doc.swagger_json_uri_relative, methods=["GET"])
        def bp_config_handler():
            request = doc.app.current_request
            return doc.get_config(request.headers["host"])

    if doc.editor:
        @bp.route(doc.editor_uri_relative(slashes=True), methods=["GET"])
        def bp_editor_handler():
            return Response(
                body=doc.editor_html,
                status_code=200,
                headers={"Content-Type": "text/html"},
            )

    @bp.route(doc.static_uri_relative + r"/{path}", methods=["GET"])
    def bp_static_handler(path):
        static_file_path = static_dir.joinpath(path)
        if static_file_path.is_file():
            content_type = "application/json"
            if static_file_path.suffix in [".png", ".ico"]:
                content_type = "image/png"
            if static_file_path.suffix in [".jpg", ".jpeg"]:
                content_type = "image/jpeg"
            if static_file_path.suffix in [".css"]:
                content_type = "text/css"
            if static_file_path.suffix in [".js"]:
                content_type = "text/javascript"
            return Response(
                body=static_file_path.read_bytes(),
                status_code=200,
                headers={"Content-Type": content_type},
            )
        return NotFoundError(path)

    doc.app.register_blueprint(bp, url_prefix=doc.url_prefix)


def match(doc):
    try:
        from chalice import Chalice
        if isinstance(doc.app, Chalice):
            return handler
    except ImportError:
        pass
    return None
