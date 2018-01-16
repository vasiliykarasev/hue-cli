#!/usr/bin/python2
from __future__ import print_function
import argparse
from phue import Bridge
import os, sys

class Executor:
    COMMANDS_ZERO_ARGS = ['on', 'off', 'dim', 'bright', 'dimmest']
    COMMANDS_WITH_ARGS = ['brightness']
    COMMANDS = COMMANDS_ZERO_ARGS + COMMANDS_WITH_ARGS
    bridge = None

    def __init__(self):
        bridge_ip = os.getenv('HUE_BRIDGE_IP')
        if bridge_ip is None:
            raise Exception('Could not get HUE_BRIDGE_IP environment variable, '
                            'did you forget to set it?')
        self.bridge = Bridge(bridge_ip)
        self.bridge.connect()
        return

    def __set_brightness(self, value):
        [setattr(l, 'brightness', value) for l in self.bridge.lights]

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

    def brightness(self, value):
        self.on()
        value = 254 if value is None else min(max(1, int(value)), 254)
        self.__set_brightness(value)

    @staticmethod
    def call(command, value):
        if command in Executor.COMMANDS_ZERO_ARGS:
            getattr(Executor(), args.command)()
        elif command in Executor.COMMANDS_WITH_ARGS:
            getattr(Executor(), args.command)(args.value)
        else:
            raise Exception('Did not recognize command -- looks like '
                            'something is not working right.')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=Executor.COMMANDS)
    parser.add_argument('value', nargs='?', default=None)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    Executor.call(args.command, args.value)
