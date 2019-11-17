#!/usr/bin/env python
'''
Description: 
    The contact test verifies that the chip pins have no open
    circuit or short circuit faults. The contact test also verifies
    that the device interface board (DIB) is firmly connected to
    both the tester and to the device under test (DUT).

Procedure:
    1. Set all device input pins to 0 VDC.
    2. Force a current of Ifb = 250uA.
    3. Measure the voltage Vpin on the pin under test.
'''
__author__ = "Victoria (Rice) Rodriguez"
__email__ = "rice.rodriguez@ttu.edu"
__status__ = "Prototype"

import pyvisa
import logging
import argparse
from resources import SMUSetup

class ContactTest:
    def get_valid_pins(pin_vals):
        return [f'pin {i+1}' for i,pin in enumerate(pin_vals) if pin != 'VCC' and pin != 'GND']
    
    def __init__(self,pins):
        self.rm = pyvisa.ResourceManager()
        self.list_resources = self.rm.list_resources()
        # logging.info('All resources:\n',pprint.pformat(self.list_resources))
        self.msg = 'Please ground all input pins of the DUT.'
        self.instr = SMUSetup(src='curr',lev='250e-6',sens='volt')
        self.smu = self.instr.smu
        # List of measurements for each pin
        self.meas = dict.fromkeys(pins)

    # Test on single pin
    def execute_test_pin(self,pin,last=False):
        # Turn the output on
        self.smu.write('outp on')
        # Only get the value we want
        self.smu.write(f'form:elem volt')
        # Read the voltage
        res = self.smu.query('read?')
        if last:
            self.smu.write('*rst;outp off;*cls')
            self.rm.close()
            
        self.meas[pin] = float(res)
        return res

    # Test the whole DUT
    def execute_test(self,numpins):
        self.res = []
        for pin in range(1,numpins):
            # Turn the output on
            self.smu.write('outp on')
            # Read the voltage
            res = self.smu.query('read?')
            self.res.append(res)
            sel = input('Please move the SMU probe to the next pin (NOT VCC or GND).\nType \'c\' to continue once you have done this.')
            if sel.lower() == 'c':
                print('Continuing.')
                continue
            elif self.lower() == 'q':
                print('Exiting.')
                break
            else:
                print('Unknown command. Assuming you mistyped \'c\'')
                continue
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The contact test verifies that the chip pins have no open circuit or short circuit faults. The contact test also verifies that the device interface board (DIB) is firmly connected to both the tester and to the device under test (DUT)')
    parser.add_argument('--verbose','-v',action='store_true',help='output verbosely')
    args = parser.parse_args()

    # Verbose option sets logging level to debug instead of warning
    if (args.verbose):
        logging.basicConfig(level=logging.DEBUG)
        # logging.setLevel(logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)
        # logging.setLevel(logging.WARNING)

    con = ContactTest()
    con.execute_test_pin()
