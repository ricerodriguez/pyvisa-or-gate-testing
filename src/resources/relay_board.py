#!/usr/bin/env python
'''
Description: Interfaces with the relay board. Adapted from Ian Kriner.
'''
__author__ = "Victoria (Rice) Rodriguez"
__credits__ = "Ian Kriner"
__email__ = "rice.rodriguez@ttu.edu"
__status__ = "Prototype"

import serial
from time import sleep
import serial.tools.list_ports as list_ports

class RelayBoard:
    def __init__(self,mode=None):
        self.device = serial.Serial('COM1',9600)
        if self.device is None:
            raise IOError("Could not find an Arduino. Check the connection.")
        self.set_relay(0)


    def set_pins(self,list_pins,temp=None):
        pins = '0000000000000000'
        for pin in list_pins:
            try:
                pins = pins[:pin-1]+'1'+pins[pin:]
            except IndexError:
                raise ValueError('Use indexing that starts at 1.')

        if temp is None:
            self.pins = int(pins,2)
        else:
            return int(pins,2)

    def test_cases(self,r):
        self.device.reset_input_buffer()
        self.device.write('t{}'.format(r).encode('utf-8'))
        self.device.readline()

    # i is a number between 1 and 16
    def set_relay(self,i):
        self.device.reset_input_buffer()
        self.device.write('s{}'.format(i).encode('utf-8'))
        # self.device.readline()

    def read_inputs(self):
        self.device.reset_input_buffer()
        sleep(.05)
        self.device.write('o'.encode('utf-8'))
        sleep(.05)
        c = self.device.read(4)
        # self.device.readline()
        return c

    # Turns on multiple relays, very finicky about sending data.
    def multirelay(self,list_pins=None):
        self.device.reset_input_buffer()
        if list_pins is None and self.pins is None:
            raise ValueError('No pin set up has been defined. Either use the set_pins function or provide a list of pins you\'d like to activate into the parameters of this function.')
        elif list_pins is None:
            self.device.write('*{}'.format(self.pins).encode('utf-8'))
            # self.device.readline()
        else:
            num=self.set_pins(list_pins,True)
            self.device.write('*{}'.format(num).encode('utf-8'))
            # self.device.readline()
