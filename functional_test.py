#!/usr/bin/env python
'''
Description:
    The functional test makes sure that the truth table for the chosen device
    maps out.

Procedure:
    1. Set the input pins to the configuration necessary for an output logic high
    2. Read the output pin under test to make sure the inputs produce the right
        output
    3. Set the pins to the configurationnecessary for an output logic LOW
    4. Read the output pin under test to make sure the inputs produce the right
        output
Outcomes:
    Passing Condition: all of the outputs are correct for all the output pins
    Failing Condition: at least one of the outputs is wrong for any of the
        output pins

'''
__author__ = "Isaac Morales"
__email__ = "isaac.morales@ttu.edu"
__status__ = "Prototype"

import pyvisa
import logging
import argparse as arg
from resources import SMUSetup


class FunctionalTest:
    def __init__(self,relay,pins = [None *16]):
        self.rm = pyvisa.ResourceManager()
        self.msg = 'Please make sure the connections are stable.'
        self.instr = SMUSetup('volt',vcc,'curr')
        self.smu = self.instr.smu
        self.res = None
        self.outcome = None
        self.meas = {}

        self.relay = relay

    def execute_test(self)
        # find a way to alternate which input gets logic high
        # this test will focus on two input pins at a time, so four calls/ chip
        # cycle through the truth table
        for i in range(0,4):
            readings = int(self.relay.read_input(), base = 2)
            # write i to the input pins and measure the digital status of output
            reformat = '{0:02b}'.format(i)  #make the index a binary string of 2 bits
            expected = bool(reformat[0]) | bool(reformat[1])  #use logic
            if '{0:1b}'.format(expected) != '{0:1b}'.format(readings):
                # cause a scene sis
                status = 'fail' #maybe don't do this? ask rice
                self.outcome = False
                # return status
            else:
                status = 'pass'
                self.outcome = True
                # return status
if __name__ == '__main__':
    main()
