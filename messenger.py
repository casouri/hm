try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print(
        'Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using "sudo" to run your script'
    )
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class GPIOMessenger():
    '''messenger that transmit message through raspberry pi RPIO

    Provides basic abstractions(set up, send hign/low signal) for subclasses that specifically implement different mesages

    This class is meant to be overwrited by subclass

    Must call cleanup action before program exits


    send method should be kept untouched

    Properties:
        pin (int): a GPIO pin used
    '''

    pin = 11
    commonResponse = 'Action OK'

    def __init__(self):
        '''init'''
        GPIO.setmode(GPIO.BOARD)

    def send(self, action):
        '''send message

        Args:
            action (dict): {'action': 'some-action, 'kwargs': {'kwargs'(optional)}}
        '''
        operation = action['action']
        if 'arguments' in action:
            kwargs = action['kwargs']
        else:
            kwargs = {}
        response = self.actionBook[operation](self, **kwargs)
        return response

    def _switchOn(self):
        GPIO.output(self.pin, True)
        logger.info('switched on')
        return self.commonResponse

    def _switchOff(self):
        GPIO.output(self.pin, False)
        logger.info('switched off')
        return self.commonResponse

    def _getStatus(self):
        '''gets the other end's status

        Returns:
            str: {"status name": 'status'}
        '''
        # you can treat a output pin as a input pin
        # when you want to know the status
        if GPIO.input(self.pin):
            onoffStatus = 'on'
        else:
            onoffStatus = 'off'

        return '{"onoff": onoffStatus}'

    def _cleanup(self):
        GPIO.cleanup()
        return self.commonResponse

    actionBook = {
        'switch-on': _switchOn,
        'switch-off': _switchOff,
        'get-status': _getStatus,
        'cleanup': _cleanup
    }


class HardSwitchMessenger(GPIOMessenger):
    '''messenger for switches that can be either turned on or off

    Needs one pin
    '''

    def __init__(self, pin):
        '''init

        Args:
            pins (list): GPIO pins to use on raspberry pi
       '''
        self.super().__init__(pin)
        GPIO.setup(pin, GPIO.OUT)


if __name__ == '__main__':
    messenger = GPIOMessenger([11])
    messenger.switchOn()
