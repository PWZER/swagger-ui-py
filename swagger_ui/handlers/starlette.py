def handler(doc):
    from starlette.responses import HTMLResponse, JSONResponse
    from starlette.staticfiles import StaticFiles

    async def swagger_doc_handler(request):
        return HTMLResponse(content=doc.doc_html, media_type='text/html')

    async def swagger_editor_handler(request):
        return JSONResponse(content=doc.editor_html, media_type='text/html')

    async def swagger_config_handler(request):
        host = '{}:{}'.format(request.url.hostname, request.url.port)
        return JSONResponse(doc.get_config(host))

    doc.app.router.add_route(
        doc.root_uri_absolute(slashes=True), swagger_doc_handler,
        ['get'], 'swagger-ui',
    )
    doc.app.router.add_route(
        doc.root_uri_absolute(slashes=False), swagger_doc_handler,
        ['get'], 'swagger-ui',
    )

    if doc.editor:
        doc.app.router.add_route(
            doc.editor_uri_absolute(slashes=True), swagger_doc_handler,
            ['get'], 'swagger-editor',
        )
        doc.app.router.add_route(
            doc.editor_uri_absolute(slashes=False), swagger_doc_handler,
            ['get'], 'swagger-editor',
        )

    doc.app.router.add_route(
        doc.swagger_json_uri_absolute, swagger_config_handler,
        ['get'], 'swagger-config',
    )
    doc.app.router.mount(
        doc.static_uri_absolute,
        app=StaticFiles(directory='{}/'.format(doc.static_dir)),
        name='swagger-static-files',
    )


def match(doc):
    try:
        import starlette.applications
        if isinstance(doc.app, starlette.applications.Starlette):
            return handler
    except ImportError:
        pass
    return None
