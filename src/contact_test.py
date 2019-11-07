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
import pprint

class ContactTest:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.list_resources = self.rm.list_resources()
        logging.info('All resources:\n',pprint.pformat(self.list_resources))
        self.msg = 'Please ground all input pins of the DUT.'
        self.smu = None
        self.res = None
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
        self.smu.write('*rst;outp off;*cls')
        # Set the current to 250 uA
        self.smu.write('sour:curr:lev 250e-6')
        # Set the source mode to current
        self.smu.write('sour:func:mode curr')
        # Set the sensing mode to voltage
        self.smu.write('sens:func "volt"')
        # Turn the output on
        self.smu.write('outp on')

        # Read the voltage
        self.res = self.smu.query('read?')
        self.rm.close()
        return self.res
        

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
    con.execute_test()
