import messenger


class Accessory():
    '''abstract class for accessories'''
    messengerBook = {'hard-switch-messenger': messenger.HardSwitchMessenger}


class Switch():
    '''a switch. Only have on and off status. Meant to be overwrited by subclasses

    must call cleanup action at exit when using any GPIO messenger

    '''

    def __init__(self,
                 name,
                 messenger,
                 messengerKWArgs,
                 description='no description'):
        '''init

        Args:
            name (str): the name of the swtich, e.g.: lamp
            messenger (str): messenger used to ask the actual object to perform action
            messengerKArgs (dict): the keyword arguments used to construct messenger instance
            description (str): default to "no description". describe the switch, e.g.: my desktop lamp
        '''
        self.name = name
        self.messenger = self.messengerBook[messenger](**messengerKWArgs)
        self.discription = description

    def act(self, action):
        '''take an action

        Args:
            action (dict): {'action':'action name', 'kwargs': {'kwargs' (optional)}}
        '''
        response = self.messenger.send(action)
        return response
