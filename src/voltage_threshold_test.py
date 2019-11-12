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
__author__ = "Isaac Morales"
__email__ = "isaac.morales@ttu.edu"
__status__ = "Prototype"


import pyvisa
import logging
import argparse as arg
from resources import SMUSetup

class VoltageThreshold:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.list_resources = self.rm.list_resources()
        logging.info('All resources:\n',pprint.pformat(self.list_resources)
        self,msg = 'Please make sure you connected one input pin and one output pin'
        self.instr = SMUSetup('volt', 0 ,'volt')
        self.smu = self.instr.smu
        self.res = None


    def execute_test(self, Vcc, pinStart):
        pinOut = 0
        Vin = 0
            #reset,set to preset,clear
        self.smu.write('*rst;outp off;*cls')
        if pinStart:    #if we're starting at 1
            Vin = Vcc      #slowly move our way down from VCC
            self.smu.write('sour:func:mode: volt')
            for thresh in range(Vin, 0, -.1):
                self.smu.setup('volt', thresh, 'curr')
                self.smu.write('outp on')
                if pinOut == 0: 
                    return thresh
                else:
                     continue
        else:
            Vin = 0
            for thresh in range(Vin, Vcc, .1):
                self.smu.setup('volt', thresh, 'curr')
                self.smu.write('outp on')
                if pinOut == 1:
                    return thresh
                else:
                    continue


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

    Vcc = input('What is the Vcc of your device? \n')
    pinStart = bool(input('What are you starting the input pin at? 1 or 0 \n'))


    vt = VoltageThreshold()
    Threshold =  vt.execute_test(Vcc,pinStart)
    # print('Threshold')
