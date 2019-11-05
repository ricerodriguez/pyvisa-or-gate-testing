#!/usr/bin/env python
'''

Description:
    The Voltage Threshold test determines the minimum input Voltage
    required to cause the device output to switch from high to low

Procedure:
    1. Write an input pattern to the device that results in a logic 0 on
    the input pin under test and also propagates that 0 across to an output pin

    2. Increase the voltage level on the input pin in steps of .1 VDC

    3. If the device produces and error, record the input voltage as Vil

    4. Write an input pattern to the device that results in a logic 1 on
    the input pin under test and also propagates that 1 across to an output pin

    5. Decrease the voltage level on the input pin in steps of .1 VDC

    6. If the device produces and error, record the input voltage as Vih

'''
__author__ = "Victoria (Rice) Rodriguez, Isaac Morales"
__email__ = "rice.rodriguez@ttu.edu, isaac.morales@ttu.edu"
__status__ = "Prototype"


import pyvisa
import logging
import argparse as arg

class VoltageThreshold:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.rm.list.resources()
        self.smu = None
        self.__smuConfig(self)

    def __smuConfig(self):
        try:
            self.smu = rm.open_resource('')[0]
            self.smu.read_termination = '\n'
            self.smu.write_termination = '\n'
            logging.debug('set SMU as {}'.format(self.smu))
            self.smu.query('*IDN')
            logging.info('Queried SMU for IDN and received the following message back: \n',
                        self.smu.read_bytes(1))

        except Exception as err:
            logging.error('Make sure everything is connected correctly! :)')
            exit()
'''
    def findThresh(self, Vcc, pinStart):
        pinOut = i'm sure theres a way to read this pin value as a bool value
        Vin = 0
        if pinStart:
            Vin = Vcc
            for thresh in range(Vin, 0, -.1):
                if pinOut == 0:
                    return thresh
                else:
                     continue
        else:
            Vin = 0
            for thresh in range(Vin, Vcc, .1):
                if pinOut == 1:
                    return thresh
                else:
                    continue
'''

if __name__ == '__main__':
    parser = arg.ArgumentParser(description = 'Voltage Threshold Test finds the minimum input Voltage'
                                          'required to cause the device output to switch from high to low')
    parser.add_argument('--verbose','-v', action = 'store_true', help = 'output verbosely')
    args = parser.parse_args()

    #if verbose is set, set logging level to debug, instead of warning
    if (args.verbose):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    Vcc = float(input('What is the Vcc of your device? \n'))
    pinStart = bool(input('What are you starting the input pin at? 1 or 0 \n'))


    vt = VoltageThreshold()
    #Threshold =  vt.findThresh(Vcc,pinStart)
    # print('Threshold')
