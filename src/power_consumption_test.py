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
__author__ = "Victoria (Rice) Rodriguez, Isaac Morales"
__email__ = "rice.rodriguez@ttu.edu, isaac.morales@ttu.edu"
__status__ = "Prototype"

import pyvisa
import logging
import argparse

class PowerConsumptionTest:
    def __init__(self):
        rm = pyvisa.ResourceManager()
        logging.info('All resources:\n',rm.list_resources())
        self.msg = 'Please disconnect all output pins from the DUT and connect the SMU to the VCC pin.'
        self.smu = None
        self.__config_instr(rm)

    def __config_instr(self,rm):
        # First get the SMU from the list of resources
        try:
            self.smu = rm.open_resource(rm.list_resources()[-1])
            self.smu.read_termination = '\n'
            self.smu.write_termination = '\n'
            logging.debug('Set SMU as {}'.format(self.smu))
            self.smu.write('*IDN?')
            # If it times out, it is broken. I don't know what it times out with.
            logging.info('Queried SMU for IDN and received the following message back:\n',
                         self.smu.read_bytes(1))
        except IndexError as err:
            logging.error('No instruments are connected to the computer. Please try again.')
            exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Power Consumption Test finds the worst-case power consumption'
                                     'for both static and dynamic operational conditions.')
    parser.add_argument('--verbose','-v',action='store_true',help='output verbosely')
    args = parser.parse_args()

    # Verbose option sets logging level to debug instead of warning
    if (args.verbose):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    pct = PowerConsumptionTest()
