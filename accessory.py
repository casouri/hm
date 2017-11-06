try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print(
        'Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using "sudo" to run your script'
    )
import log

logger = log.setupLog(__name__, 'debug')


class Switch():
    '''a switch. Only have on and off status. Meant to be overwrited by subclasses

    For sucbclasses, implement actions in actionBook and add implementations to action book

    '''
    actionBook = {'switch-on': None, 'switch-off': None}
    commonResponse = 'Action OK'

    def __init__(self, name: str, description: str='no description') -> None:
        '''init

        Args:
            name (str): the name of the swtich, e.g.: lamp
            description (str): default to "no description". describe the switch, e.g.: my desktop lamp
        '''
        self.name = name
        self.discription = description

    def act(self, action: str, kwargs: dict={}):
        '''take an action

        Args:
            action (str): action name
            kwargs (dict): default {}. Any possible keyword arguments
        '''
        response = self.actionBook[action](self, **kwargs)
        return response


class GPIOSwitch(Switch):
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
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)

    def _switchOn(self) -> str:
        GPIO.output(self.pin, True)
        logger.info('switched on')
        return self.commonResponse

    def _switchOff(self) -> str:
        GPIO.output(self.pin, False)
        logger.info('switched off')
        return self.commonResponse

    def _getStatus(self) -> str:
        '''gets the switch's status

        Returns:
            str: {"onoff": 'status'}
        '''
        # you can treat a output pin as a input pin
        # when you want to know the status
        if GPIO.input(self.pin):
            onoffStatus = 'on'
        else:
            onoffStatus = 'off'

        return '\{"onoff": {}\}'.format(onoffStatus)

    def _cleanup(self) -> str:
        GPIO.cleanup(self.pin)
        return self.commonResponse

    actionBook = {
        'switch-on': _switchOn,
        'switch-off': _switchOff,
        'get-status': _getStatus,
        'cleanup': _cleanup
    }
