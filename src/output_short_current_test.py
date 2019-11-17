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
Ideas:
    1: short the output pin to ground
    2: start with A,B = 0  then set the voltage to vcc for one of the inputs.
    3: measure the current at the output pin.
Outcomes:
    Passing Condition: Ioh >= .04 A
    Failing Condition: Ioh < .04 A

Author's note:
    so far i think we're going to make one input logic high bc it's less work
    then we're going to physically ground all the output pins.
    for the circuitry we're grouding and measuring the outputs

Adapted from code by Victoria Rodriguez
        I wonder what we should do about the PSU
'''

__author__ = "Isaac Morales"
__credits__ = "Victoria Rodriguez"
__email__ = "isaac.morales@ttu.edu"
__status__ = "Prototype"

import pyvisa
import logging
import argparse
from resources import SMUSetup

class OutputShortCurrentTest:
    def get_valid_pins(pin_vals):
        return [f'pin {i+1}' for i,pin in enumerate(pin_vals) if pin == 'OUT']

    def __init__(self,pin_vals):
        self.rm = pyvisa.ResourceManager()
        self.msg = 'Please disconnect all output pins from the DUT and connect the SMU to the input pin.'
        self.instr = SMUSetup(src='volt',lev=0,sens='curr')
        self.smu = self.instr.smu
        self.meas = dict.fromkeys(OutputShortCurrentTest.get_valid_pins(pin_vals))
        self.outcomes = dict.fromkeys(OutputShortCurrentTest.get_valid_pins(pin_vals))

        #basically the same as the power consumption test
    def execute_test(self,pin,last=False):
        # if not vcc is None:
        #     self.instr.setup('volt',vcc,'curr')
        #turn the output on
        logging.debug(f'Outputting 0V from SMU')
        self.smu.write('outp on')
        self.smu.write('form:elem curr')
        res = self.smu.query('read?')
        if last:
            self.smu.write('*rst;outp off;*cls')
            self.rm.close()

        # logging.warning('read: {}'.format(self.res))
        logging.info(f'Output Short Current Test for {pin.capitalize()}: {res}')
        fres = float(res)
        self.meas[pin] = fres
        self.outcomes[pin] = fres >= 0.04


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

    ost = OutputScTest(5)
    logging.warning('vcc is 5')
    ost.execute_test()
    # print(Ires)
    # ost.document(boom)
