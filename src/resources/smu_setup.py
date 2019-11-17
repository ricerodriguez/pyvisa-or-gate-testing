#!/usr/bin/env python
'''
Description: 
    This class contains the function to setup the SMU, which
    is used in several of the tests that are needed.

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

class SMUSetup:
    def __init__(self,src,lev,sens,rm=pyvisa.ResourceManager()):
        self.rm = rm
        self.smu = None
        self.res = None
        self.__verify()
        self.setup(src,lev,sens)

    # Verify that the instrument is connected and communication is able to take place
    def __verify(self):
        # First get the SMU from the list of resources
        try:
            self.smu = self.rm.open_resource('SMU2400')
            self.smu.read_termination = '\n'
            self.smu.write_termination = '\n'
            logging.debug('Set SMU as %(self.smu)s')
            bytes_back=self.smu.query('*IDN?')
            logging.debug('Received identity of SMU as: %(bytes_back)s')

        except AttributeError as err:
            logging.error(err)
            logging.error('Please connect to the SMU.')
            exit(-1)

        except pyvisa.errors.VisaIOError as err:
            logging.error(err)
            logging.error('Please connect to the SMU.')
            exit(-1)

    # mode = source mode, lev = how much to source, sens = sens mode
    def setup(self,src,lev,sens):
        try:
            # First reset and clear status
            self.smu.write('*rst;outp off;*cls')
            # Set the source mode
            self.smu.write(f'sour:func:mode {src}')
            # Set the level of the source
            self.smu.write(f'sour:{src}:lev {lev}')
            # Set the sensing mode
            self.smu.write(f'sens:func "{sens}"')
            # Only get the value we want
            self.smu.write(f'form:elem {sens}')

        except pyvisa.errors.VisaIOError as err:
            logging.error('Please connect to the SMU.')
            logging.error(err)
