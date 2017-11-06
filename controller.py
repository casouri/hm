# import accessory
import testAccessory
import json
import log

# configure logging
logger = log.setupLog(__name__, 'debug')
'''every accessory have to take name argument as first argument'''


class Controller():
    '''control all the behaviors of accessories'''
    accessoryBook = {}

    # TODO
    # accessoryConstructorBook = {'hard-switch': accessory.Switch}
    accessoryConstructorBook = {'hard-switch': testAccessory.TestGPIOSwitch}

    def __init__(self):
        self.createAcceccories()

    def createAcceccories(self):
        with open('config.json') as f:
            accessoryConfigBook = json.load(f)['accessory']
            logger.debug('accessoryConfigBook: {}'.format(accessoryConfigBook))

        # create objects and put into book
        for name in accessoryConfigBook:
            accessoryConfig = accessoryConfigBook[name]
            constructorName = accessoryConfig['accessory-type']
            constructor = self.accessoryConstructorBook[constructorName]

            if 'kwargs' not in accessoryConfig:
                kwargs = {}
            else:
                kwargs = accessoryConfig['kwargs']

            self.accessoryBook[name] = constructor(name, **kwargs)
