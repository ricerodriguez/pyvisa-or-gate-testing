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

class PowerConsumptionTest:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.smu = None
        self.__config_instr()

    def __config_instr(self):
        # First get the SMU from the list of resources
        try:
            self.smu = rm.list_resources()[0]
            logging.debug("Set SMU as {}".format(self.smu))
        except IndexError as err:
            logging.error("No instruments are connected to the computer. Please try again.")
            exit()
            
