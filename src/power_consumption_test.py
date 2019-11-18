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
    def get_valid_pins(pin_vals):
        return [f'pin {i+1}' for i,pin in enumerate(pin_vals) if pin == 'VCC']
    
    def __init__(self,rm,vcc,pin_vals):
        self.rm = rm
        self.msg = 'Please disconnect all output pins from the DUT and connect the SMU to the VCC pin.'
        self.instr = SMUSetup(src='volt',lev=vcc,sens='curr',rm=rm)
        self.smu = self.instr.smu
        # List of measurements for each pin
        self.meas = dict.fromkeys(PowerConsumptionTest.get_valid_pins(pin_vals))
        
    # Actually perform the test
    def execute_test(self,pin,vcc=None,last=False):
        if not vcc is None:
            self.instr.setup('volt',vcc,'curr')
        # Turn the output on
        self.smu.write('outp on')
        # Only get the value we want
        self.smu.write('form:elem curr')
        # Read the current
        res = self.smu.query('read?')
        if last:
            self.smu.write('*rst;outp off;*cls')
        #     self.rm.close()

        self.meas[pin] = float(res)
        return res
        

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
    print(pct.execute_test())
