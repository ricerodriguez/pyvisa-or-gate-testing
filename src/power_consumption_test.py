#!/usr/bin/env python
'''
Description: 
    Power Consumption Test finds the worst-case power consumption for
    both static and dynamic operational conditions.

Procedure:
    1. Set all device output pins to be open circuit.
    2. Set the power supply pin to its recommended V_CC.
    3. Measure the current draw I_CC from the power supply pin.
'''
__author__ = "Victoria (Rice) Rodriguez"
__email__ = "rice.rodriguez@ttu.edu"
__status__ = "Prototype"

import pyvisa
import logging
import argparse
from resources import SMUSetup

class PowerConsumptionTest:
    def __init__(self,vcc):
        self.rm = pyvisa.ResourceManager()
        self.msg = 'Please disconnect all output pins from the DUT and connect the SMU to the VCC pin.'
        self.instr = SMUSetup('volt',vcc,'curr')
        self.smu = instr.smu
        self.res = None

    # Actually perform the test
    def execute_test(self,vcc=None):
        if not vcc is None:
            self.instr.setup('volt',vcc,'curr')
        # Turn the output on
        self.smu.write('outp on')
        # Read the voltage
        self.res = self.smu.query('read?')
        self.smu.write('*rst;outp off;*cls')
        return self.res
        self.rm.close()
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Power Consumption Test finds the worst-case power consumption'
                                     'for both static and dynamic operational conditions.')
    parser.add_argument('--verbose','-v',action='store_true',help='output verbosely')
    args = parser.parse_args()

    # Verbose option sets logging level to debug instead of warning
    if (args.verbose):
        logging.basicConfig(level=logging.DEBUG)
        # logging.setLevel(logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)
        # logging.setLevel(logging.WARNING)

    pct = PowerConsumptionTest(5)
    pct.execute_test()
