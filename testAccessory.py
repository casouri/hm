import log

logger = log.setupLog(__name__, 'debug')


class TestGPIOSwitch():
    '''a test switch. Only have on and off status'''

    commonResponse = 'Action OK'

    def __init__(self,
                 name: str,
                 description: str='no description',
                 pin: int=11) -> None:
        '''init

        Args:
            name (str): the name of the swtich, e.g.: lamp
            description (str): default to "no description". describe the switch, e.g.: my desktop lamp
            pin (int): the pin number of the gpio pin you want to use.
        '''

    def act(self, action: str, kwargs: dict={}) -> str:
        '''take an action

        Args:
            action (str): {'action':'action name', 'kwargs': ['kwargs' (optional)]}
            kwargs (dict): default {}. Any possible keyword arguments
        '''
        logger.debug(action)
        response = self.actionBook[action](self, **kwargs)
        return response

    def _switchOn(self) -> str:
        return self.commonResponse

    def _switchOff(self) -> str:
        return self.commonResponse

    def _getStatus(self) -> str:
        '''gets the switch's status

        Returns:
            str: {"onoff": 'status'}
        '''
        # you can treat a output pin as a input pin
        # when you want to know the status
        onoffStatus = 'on or off? Who knows'
        return ('{"onoff": "%s"}' % onoffStatus)

    def _cleanup(self) -> str:
        return self.commonResponse

    actionBook = {
        'switch-on': _switchOn,
        'switch-off': _switchOff,
        'get-status': _getStatus,
        'cleanup': _cleanup
    }
