def handler(doc):
    from aiohttp import web

    async def swagger_doc_handler(request):
        return web.Response(text=doc.doc_html, content_type='text/html')

    async def swagger_editor_handler(request):
        return web.Response(text=doc.editor_html, content_type='text/html')

    async def swagger_config_handler(request):
        return web.json_response(doc.get_config(request.host))

    doc.app.router.add_get(doc.uri(), swagger_doc_handler)
    doc.app.router.add_get(doc.uri(r'/'), swagger_doc_handler)

    if doc.editor:
        doc.app.router.add_get(doc.uri(r'/editor'), swagger_editor_handler)
        doc.app.router.add_get(doc.uri(r'/editor/'), swagger_editor_handler)

    doc.app.router.add_get(doc.uri(r'/swagger.json'), swagger_config_handler)
    doc.app.router.add_static(doc.uri(r'/'), path='{}/'.format(doc.static_dir))


def match(doc):
    try:
        import aiohttp.web
        if isinstance(doc.app, aiohttp.web.Application):
            return handler
    except ImportError:
        pass
    return None
