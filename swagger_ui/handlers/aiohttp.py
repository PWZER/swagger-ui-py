def handler(doc):
    from aiohttp import web

    async def swagger_doc_handler(request):
        return web.Response(text=doc.doc_html, content_type='text/html')

    async def swagger_editor_handler(request):
        return web.Response(text=doc.editor_html, content_type='text/html')

    async def swagger_config_handler(request):
        return web.json_response(doc.get_config(request.host))

    doc.app.router.add_get(
        doc.root_uri_absolute(slashes=True), swagger_doc_handler)
    doc.app.router.add_get(
        doc.root_uri_absolute(slashes=False), swagger_doc_handler)

    if doc.editor:
        doc.app.router.add_get(
            doc.editor_uri_absolute(slashes=True), swagger_editor_handler)
        doc.app.router.add_get(
            doc.editor_uri_absolute(slashes=False), swagger_editor_handler)

    doc.app.router.add_get(
        doc.swagger_json_uri_absolute, swagger_config_handler)
    doc.app.router.add_static(doc.static_uri_absolute, path=doc.static_dir)


def match(doc):
    try:
        import aiohttp.web
        if isinstance(doc.app, aiohttp.web.Application):
            return handler
    except ImportError:
        pass
    return None
