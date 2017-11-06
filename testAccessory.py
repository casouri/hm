class TestMessenger():
    '''test messenger that transmit message through raspberry pi RPIO

    Provides basic abstractions(set up, send hign/low signal) for subclasses that specifically implement different mesages

    This class is meant to be overwrited by subclass

    send method should be kept untouched

    Must call cleanup action before program exits

    every action return a response string

    Properties:
        pins (list): a list ot GPIO pins used
    '''
    commonResponse = 'Action OK'

    def __init__(self, pins):
        self.pins = pins

    def send(self, action):
        '''send message

        Args:
            action (dict): {'action', ['kwargs'(optional)]}
        '''
        operation = action['action']
        if 'kwargs' in action:
            kwargs = action['kwargs']
        else:
            kwargs = {}

        # actual working
        response = self.actionBook[operation](self, **kwargs)
        return response

    def _switchOn(self):
        print('switched on')
        return self.commonResponse

    def _switchOff(self):
        print('swtiched off')
        return self.commonResponse

    def _getStatus(self):
        '''gets the other end's status

        Returns:
            dict: {'status name': 'status'}
        '''
        # you can treat a output pin as a input pin
        # when you want to know the status
        print('check status. I am just a test messenger')
        return 'some return'

    def _cleanup(self):
        print('cleaned up')
        return self.commonResponse

    actionBook = {
        'switch-on': _switchOn,
        'switch-off': _switchOff,
        'get-status': _getStatus,
        'cleanup': _cleanup
    }


class TestSwitch():
    '''a test switch. Only have on and off status'''
    messengerBook = {'hard-switch-messenger': TestMessenger}

    def __init__(self,
                 name,
                 messenger,
                 messengerKWArgs,
                 description='no description'):
        self.name = name
        self.messenger = self.messengerBook[messenger](**messengerKWArgs)
        self.discription = description

    def act(self, action):
        '''take an action

        Args:
            action (dict): {'action':'action name', 'kwargs': ['kwargs' (optional)]}
        '''
        response = self.messenger.send(action)
        return response


if __name__ == '__main__':
    switch = TestSwitch('lamp', 'hard-switch-messenger', {'pins': [11]},
                        'my desktop lamp')
    switch.act({'operation': 'switch-on'})
