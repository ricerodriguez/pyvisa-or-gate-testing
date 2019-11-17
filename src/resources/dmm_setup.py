#!/usr/bin/env python
'''
Description: 
    This class contains the function to setup the DMM, which
    is used in the Voltage Threshold Test.

Procedure:
    1. Check if device responds to query for identity.
    2. Turn everything off and clear the screen.
    3. Set the source mode.
    4. Set the level of the source.
    5. Set the sense mode.
'''
__author__ = "Victoria (Rice) Rodriguez"
__email__ = "rice.rodriguez@ttu.edu"
__status__ = "Prototype"

import pyvisa
import logging

class DMMSetup:
    def __init__(self,sens):
        self.rm = pyvisa.ResourceManager()
        self.dmm = None
        self.__verify()
        self.setup(sens)

    # Verify that the instrument is connected and communication is able to take place
    def __verify(self):
        # First get the SMU from the list of resources
        try:
            # 
            self.dmm = self.rm.open_resource('DMM')
            self.dmm.read_termination = '\n'
            self.dmm.write_termination = '\n'
            logging.debug('Set DMM as %(self.dmm)s')
            bytes_back=self.dmm.query('*IDN?')
            logging.debug('Received identity of DMM as: %(bytes_back)s')

        except AttributeError as err:
            logging.error(err)
            logging.error('Please connect to the DMM.')
            exit(-1)

        except pyvisa.errors.VisaIOError as err:
            logging.error(err)
            logging.error('Please connect to the DMM.')
            exit(-1)

    # mode = source mode, lev = how much to source, sens = sens mode
    def setup(self,sens):
        try:
            # First reset and clear status
            self.dmm.write('*rst;outp off;*cls')
            # Set function for what to measure
            self.dmm.write(f'func "{sens}:dc"')
            # Set to autorange
            self.dmm.write(f'{sens}:rang:auto on')

            # # Set the source mode
            # self.smu.write(f'sour:func:mode {src}')
            # # Set the level of the source
            # self.smu.write(f'sour:{src}:lev {lev}')
            # Set the sensing mode
            # self.smu.write(f'sens:func "{sens}"')
            # # Only get the value we want
            # self.smu.write(f'form:elem {sens}')

        except pyvisa.errors.VisaIOError as err:
            logging.error('Please connect to the SMU.')
            logging.error(err)
