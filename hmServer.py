from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import atexit
import cgi
import ssl

import controller
import log

##############
# PROPERTIES #
##############

# configure logging
logger = log.setupLog(__name__, 'debug')

# load configuration
with open('config.json') as f:
    try:
        config = json.load(f)
    except json.decoder.JSONDecodeError as e:
        logger.error('config.json not valid')
        logger.error(e)

ADDRESS = config['address']
PORT = config['port']

# functions to be called when program exits
cleanupList = []

# controller that control all the accesories
accessoryController = controller.Controller()

PASS_WORD = config['passwd']

#############
# FUNCTIONS #
#############


# credit to http://code.activestate.com/recipes/81547-using-a-simple-dictionary-for-cgi-parameters/
def cgiFieldStorageToDict(fieldStorage) -> dict:
    """Get a plain dictionary, rather than the '.value' system used by the cgi module."""
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


def exit_handler() -> None:
    '''calls cleanup functions'''
    logger.info('Exiting')
    if len(cleanupList) != 0:
        for func in cleanupList:
            func()


class HMRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = 'Connection OK'
        self.wfile.write(bytes(message, 'utf8'))

    def do_POST(self) -> None:
        '''handle post requests

        post format: {"accessory-name": "name", "action": "some action", (optional)"kwargs": {}}'''

        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            })

        form = cgiFieldStorageToDict(form)
        logger.debug(form)

        if form['passwd'] != PASS_WORD:
            logger.warn('wrong password')
            self.wfile.write(bytes('wrong password', 'utf8'))
            return

        if all(n in form for n in ['action', 'accessory-name']):
            accessoryName, actionName = form['accessory-name'], form['action']

            if 'kwargs' in form:
                kwargs = form['kwargs']
            else:
                kwargs = {}

            logger.debug(accessoryName)
            logger.debug(actionName)
            logger.debug(kwargs)

            logger.debug(accessoryController.accessoryBook)

            # actual working
            response = accessoryController.accessoryBook[accessoryName].act(
                action=actionName, kwargs=kwargs)

            logger.debug(response)
            self.wfile.write(bytes(response, 'utf8'))
        else:
            logger.error(
                '"action" or "accessory-name" not specified in post request, which is mandatory.'
            )
            self.wfile.write(bytes('Action failed', 'utf8'))


def run() -> None:
    logger.info('Starting HM server')
    serverAddress = (ADDRESS, PORT)
    httpd = HTTPServer(serverAddress, HMRequestHandler)

    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        keyfile="root.key",
        certfile='root.crt',
        server_side=True)

    logger.info('Running server')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
        logger.info('Server closed')


if __name__ == '__main__':
    run()
