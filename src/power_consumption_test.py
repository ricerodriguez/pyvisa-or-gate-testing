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
import pprint

class PowerConsumptionTest:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.list_resources = self.rm.list_resources()
        logging.info('All resources:\n',pprint.pformat(self.list_resources))
        self.msg = 'Please disconnect all output pins from the DUT and connect the SMU to the VCC pin.'
        self.smu = None
        self.__config_instr()

    def __config_instr(self):
        # First get the SMU from the list of resources
        try:
            self.smu = self.rm.open_resource(self.list_resources[-1])
            self.smu.read_termination = '\n'
            self.smu.write_termination = '\n'
            logging.debug('Set SMU as {}'.format(self.smu))
            bytes_back=self.smu.query('*IDN?')
            # self.smu.write('*IDN?')          # Apparently write message already
            #                                  # has termination character '\n'
            # bytes_back = self.smu.read_bytes(1)
            logging.info('Queried SMU for IDN and received the following message back:\n',
                         bytes_back)
        except IndexError as err:
            logging.error(err)
            logging.error('No instruments are connected to the computer. Please try again.')
            exit(-1)

        except pyvisa.errors.VisaIOError as err:
            logging.error(err)
            exit(-1)

    # Actually perform the test
    def execute_test(self):
        # First reset, set status to preset, and clear status
        self.smu.write('*rst;status:preset;*cls')
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

    pct = PowerConsumptionTest()
    pct.execute_test()
