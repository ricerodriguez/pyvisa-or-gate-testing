#!/usr/bin/env python

'''
Description:
    The contact test verifies that the chip pins have no open circuit or short
    circuit faults. The contact test also verifies that the device interface
    board (DIB) is firmly connected to both the tester and to the device
    under test (DUT).

Procedures:
    1. Set all device inputs to 0 VDC
    2. Force a current Ifb~250uA out of the pin under test
    3. Measure the voltage Vpin on the pin under test

'''

__author__ = "Isaac Morales"
__email__ = "isaac.morales@ttu.edu"
__status__ = "Prototype"


import pyvisa
import logging
import argpase as arg
from resources import SMUSetup

class ContactTest:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.msg = 'Please disconnect all output pins from the DUT and connect the SMU to the input pin.'
        self.instr = SMUSetup('curr',0,'volt')
        self.smu = self.instr.smu
        self.res = None

    def execute_test(self,Vin):
        if not Vin i None:
            self.instr.setup('curr',Vin,'volt')

        self.smu.write('outp on')
        self.res = self.smu.query('read?')
        return self.res
        self.rm.close()
        self.smu.write('*rst;outp off;*cls;')

    def document(self,info):
        testNum = input('is this the first chip? y/n ')

        if testNum == 'y':
            reults = open("ContactTest.txt","w")
            results.write("Testing chip number: " + testNum)
            logging.debug('chip number: ' + testNum)
        else:
            results = open("ContactTest.txt","a")
            results.write("Testing chip number: " + testNum)
            logging.debug('chip number: ' + testNum)

        results.write('\n {} \n'.format(info))
        results.close()

if __name__ == '__main__':
        parser = arg.ArgumentParser(description= 'The Output Short Current Test verifies the output current drive of a'
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

        ct = ContactTest()
        info = ct.execute_test(250e-6)
        print(info)
        ct.document(info)
