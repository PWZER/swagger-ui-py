from .core import Interface


class TornadoInterface(Interface):
    def __init__(self, *args, **kwargs):
        kwargs['app_type'] = 'tornado'
        super(TornadoInterface, self).__init__(*args, **kwargs)


class AiohttpInterface(Interface):
    def __init__(self, *args, **kwargs):
        kwargs['app_type'] = 'aiohttp'
        super(AiohttpInterface, self).__init__(*args, **kwargs)


class SanicInterface(Interface):
    def __init__(self, *args, **kwargs):
        kwargs['app_type'] = 'sanic'
        super(SanicInterface, self).__init__(*args, **kwargs)


class FlaskInterface(Interface):
    def __init__(self, *args, **kwargs):
        kwargs['app_type'] = 'flask'
        super(FlaskInterface, self).__init__(*args, **kwargs)


class QuartInterface(Interface):
    def __init__(self, *args, **kwargs):
        kwargs['app_type'] = 'quart'
        super(QuartInterface, self).__init__(*args, **kwargs)


class FalconInterface(Interface):
    def __init__(self, *args, **kwargs):
        kwargs['app_type'] = 'falcon'
        super(FalconInterface, self).__init__(*args, **kwargs)


class StarletteInterface(Interface):
    def __init__(self, *args, **kwargs):
        kwargs['app_type'] = 'starlette'
        super(StarletteInterface, self).__init__(*args, **kwargs)


class BottleInterface(Interface):
    def __init__(self, *args, **kwargs):
        kwargs['app_type'] = 'bottle'
        super(BottleInterface, self).__init__(*args, **kwargs)
