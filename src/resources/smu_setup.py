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
import pprint

class SMUSetup:
    def __init__(self,alias,vcc=None):
        self.rm = pyvisa.ResourceManager()
        self.smu = None
        self.res = None
        self.__verify(alias)
        self.__setup(vcc)

    # Verify that the instrument is connected and communication is able to take place
    def __verify(self,alias):
        # First get the SMU from the list of resources
        try:
            self.smu = self.rm.open_resource(alias)
            self.smu.read_termination = '\n'
            self.smu.write_termination = '\n'
            logging.debug('Set SMU as %(self.smu)s')
            bytes_back=self.smu.query('*IDN?')
        except IndexError as err:
            logging.error(err)
            logging.error('No instruments are connected to the computer. Please try again.')
            exit(-1)

        except pyvisa.errors.VisaIOError as err:
            logging.error(err)
            exit(-1)

    def __setup(self,vcc=None):
        try:
            # First reset and clear status
            self.smu.write('*rst;outp off;*cls')
            # Set the source mode to voltage
            self.smu.write('sour:func:mode volt')
            # Set the voltage to whatever the VCC is supposed to be
            self.smu.write('sour:volt:lev %(vcc)s')
            # Set the sensing mode to current
            self.smu.write('sens:func "curr"')
        except pyvisa.errors.VisaIOError as err:
            logging.error(err)


    # Actually perform the test
    def execute_test(self,vcc=None):
        if not vcc is None:
            self.__setup(vcc)
        # Turn the output on
        self.smu.write('outp on')
        # Read the voltage
        self.res = self.smu.query('read?')
        return self.res
        self.rm.close()
        

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Power Consumption Test finds the worst-case power consumption'
#                                      'for both static and dynamic operational conditions.')
#     parser.add_argument('--verbose','-v',action='store_true',help='output verbosely')
#     args = parser.parse_args()

#     # Verbose option sets logging level to debug instead of warning
#     if (args.verbose):
#         logging.basicConfig(level=logging.DEBUG)
#         # logging.setLevel(logging.DEBUG)
#     else:
#         logging.basicConfig(level=logging.WARNING)
#         # logging.setLevel(logging.WARNING)

#     pct = PowerConsumptionTest('SMU2400',5)
#     pct.execute_test()
