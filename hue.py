import argparse
import inspect
import warnings
import os
# Syntax warnings are coming from phue.
warnings.filterwarnings(action="ignore", category=SyntaxWarning)
from phue import Bridge



class Executor:
    # We could even avoid this, but it doesn't seem necessary.
    COMMANDS = [
        'on', 'off', 'dim', 'bright', 'dimmest', 'read', 'hack', 'brightness'
    ]

    def __init__(self):
        bridge_ip = os.getenv('HUE_BRIDGE_IP')
        if bridge_ip is None:
            raise Exception(
                'Could not get HUE_BRIDGE_IP environment variable, '
                'did you forget to set it?')
        self.bridge = Bridge(bridge_ip)
        self.bridge.connect()
        return

    def __set_brightness(self, value):
        [setattr(l, 'brightness', value) for l in self.bridge.lights]

    def __set_xy(self, value):
        [setattr(l, 'xy', value) for l in self.bridge.lights]

    def on(self):
        [setattr(l, 'on', True) for l in self.bridge.lights]

    def off(self):
        [setattr(l, 'on', False) for l in self.bridge.lights]

    def bright(self):
        self.on()
        self.__set_brightness(255)

    def dim(self):
        self.on()
        self.__set_brightness(100)

    def dimmest(self):
        self.on()
        self.__set_brightness(1)

    def read(self):
        self.on()
        self.__set_brightness(254)
        self.__set_xy([0.4449, 0.4066])

    def hack(self):
        self.on()
        self.__set_brightness(100)
        self.__set_xy([0.1771, 0.060])

    def brightness(self, value):
        self.on()
        value = 254 if value is None else min(max(1, int(value)), 254)
        self.__set_brightness(value)

    @staticmethod
    def call(command, values):
        if command in Executor.COMMANDS:
            func = getattr(Executor(), args.command)
            expected_num_args = len(inspect.getfullargspec(func).args) - 1
            if len(values) != expected_num_args:
                raise Exception(('Provided an unusual number of arguments; '
                                 'expected {} but provided {}').format(
                                     expected_num_args, len(values)))
            func(*values)
        else:
            raise Exception('Did not recognize command -- looks like '
                            'something is not working right.')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=Executor.COMMANDS)
    parser.add_argument('values', nargs='*', default=[], type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    Executor.call(args.command, args.values)
