#!/usr/bin/env python
'''
Description:
    The Output Short Current Test verifies the output current drive of a
    device's output pins is sustained at both high and low output voltages

Procedure:
    1. Configure the Device so that the output pin under test will be in
    logic high
    2. Force the voltage level on the output pin under test to be 0 VDC
    3. Measure the current draw Ioh from the output pin under test


    Author's note:
        so far i think we're going to make one input logic high bc it's less work
        then we're going to physically ground all the output pins.
            for the circuitry we're grouding and measuring the outputs
        I hope rice comes back soon :(
'''

__author__ = "Isaac Morales"
__email__ = "isaac.morales@ttu.edu"
__status__ = "Prototype"

import pyvisa
import logging
import argparse
from resource import SMUSetup

class OutputScTest:
    def __init__(self,vcc):
        self.rm = pyvisa.ResourceManager()
        self.msg = 'Please disconnect all output pins from the DUT and connect the SMU to the VCC pin.'
        self.instr = SMUSetup('volt',vcc,'curr')
        self.smu = self.instr.smu
        self.res = None

        #basically the same as the power consumption test
    def execute_test(self,vcc = None):
        if not vcis None:
            self.instr.setup('volt',vcc,'curr')
        #turn the output on
        self.smu.write('outp on')
        self,res  = self.smu.query('read?')
        self.smu.write('*rst;outp off;*cls;')
        return self.res
        self.sm.close()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= 'The Output Short Current Test verifies the output current drive of a'
        'device output pins is sustained at both high and low output voltages')
    parser.add_argument('--verbose','-v',action='store_true',help='output verbosely')
    args = parser.parse_args()

    # Verbose option sets logging level to debug instead of warning
    if (args.verbose):
        logging.basicConfig(level=logging.DEBUG)
        # logging.setLevel(logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)
        # logging.setLevel(logging.WARNING)
    testNum = input('which chip are you on?')

    if tesNum == '1':
        reults = open("OutputShortCurrentTest.txt","w")
        resulst.write("Testing chip number: " + testNum)
    else:
        reults = open("OutputShortCurrentTest.txt","a")
        resulst.write("Testing chip number: " + testNum)

    ost = OutputScTest(3.3)
    boom = ost.execute_test()
    print(boom)
    results.write('\n {} \n'.format(boom))
