import logging
import sys

if sys.version_info < (3,):
    from BaseHTTPServer import BaseHTTPRequestHandler
else:
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

logger = logging.getLogger('fusion')
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

MIMETYPE = {
    '': 'application/octet-stream',  # Default
    '.py': 'text/plain',
    '.c': 'text/plain',
    '.h': 'text/plain',
    '.svg': 'image/svg+xml',
}


class _RequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def __init__(self, _app, *args, **kwargs):
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
        self._app = _app

    def log_message(self, format, *args):
        logger.info("{} - - [{}] {}".format(self.address_string(), self.log_date_time_string(), format % args))

    def do_HEAD(self):
        """Serve a HEAD request."""

    def do_GET(self):
        """Serve a GET request."""


def do_handle(_app):
    def fun(*args, **kwargs):
        return _RequestHandler(_app, *args, **kwargs)

    return fun


class Router:
    def add_get(self, param):
        pass

    def add_post(self, param):
        pass


class Application:
    def __init__(self, router=None):
        if router is None:
            router = Router()
        self._router = router  # type: Router

    @property
    def router(self):
        return self._router


class Web:
    App = Application

    @staticmethod
    def run(app, host='', port=8123, debug=False):
        if debug:
            logger.setLevel(logging.DEBUG)
        server_address = (host, port)
        httpd = ThreadingHTTPServer(server_address, lambda *args, **kwargs: _RequestHandler(app, *args, **kwargs))

        sa = httpd.socket.getsockname()
        logger.info("Serving HTTP on {} port {} ...".format(sa[0], sa[1]))
        httpd.serve_forever()
