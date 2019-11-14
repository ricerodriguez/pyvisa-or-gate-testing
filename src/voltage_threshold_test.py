#!/usr/bin/env python
'''

Description:
    The Voltage Threshold test determines the minimum input Voltage
    required to cause the device output to switch from high to low

Procedures:
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
from time import sleep

class VoltageThreshold:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.msg = 'Please make sure you connected one input pin and one output pin'
        self.instr = SMUSetup('volt', 0 ,'volt')
        self.smu = self.instr.smu
        self.smu.find_arduino('6')
        self.res = None


    def execute_test(self, Vcc, pinStart, pinPos):
#         pinOut = 0
#         Vin = 0
#             #reset,set to preset,clear
#         self.smu.write('*rst;outp off;*cls')
#         if pinStart:    #if we're starting at 1
#             Vin = Vcc      #slowly move our way down from VCC
#             self.smu.write('sour:func:mode: volt')
#             for thresh in range(Vin, 0, -.1):
#                 self.smu.setup('volt', thresh, 'curr')
#                 self.smu.write('outp on')
#                 if pinOut == 0:
#                     return thresh
#                 else:
#                      continue
#         else:
#             Vin = 0
#             for thresh in range(Vin, Vcc, .1):
#                 self.smu.setup('volt', thresh, 'curr')
#                 self.smu.write('outp on')
#                 if pinOut == 1:
#                     return thresh
#                 else:
#                     continue
# 9225 for a
# 18450 for b
        self.smu.Multirelay(pinPos)
        thresh_0, thresh_1, thresh_2, thresh_3 = 0
        if pinStart:
            start = Vcc * 10 + 1
            finish = 0
            step = -1
            readOut = 0
        else:
            start = 0
            finish = Vcc * 10 + 1
            step = 1
            readOut = 1

        for volts in range(start, finish, step):
            self.smu.setup('volt', volts/10, 'curr')
            self.smu.write('outp on')
            sleep(.025)
            read = int(self.smu.read_inputs(), base = 2)
            print(volts,read)
            if read & 0b0001 != readOut and thresh_0 == 0:
                thresh_0 = volts
            if read & 0b0010 != readOut << 1 and thresh_1 == 0:
                thresh_1 = volts
            if read & 0b0100 != readOut << 2 and thresh_2 == 0:
                thresh_2 = volts
            if read & 0b1000 != readOut << 3 and thresh_3 == 0:
                thresh_3 = volts

        self.rm.close()
        return thresh_0, thresh_1, thresh_2, thresh_3

    def document(self,info):
        testNum = input('is this the first chip? y/n ')

        if testNum == 'y':
            reults = open("VoltageThresholdTest.txt","w")
            results
            results.write("Testing chip number: " + testNum)
            logging.debug('chip number: ' + testNum)
        else:
            results = open("VoltageThresholdTest.txt","a")
            results.write("Testing chip number: " + testNum)
            logging.debug('chip number: ' + testNum)

        results.write('\n {} \n'.format(info))
        results.close()



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
    pinStart = bool(input('Are starting with an output of 1 or 0? \n'))
    choice = input('are you testing pins A or B? \n')
    if choice == 'A':
        pinPos = 9225
    elif choise == 'B':
        pinPos = 18450



    vt = VoltageThreshold()
    Thresholds =  vt.execute_test(Vcc,pinStart,pinPos)
    vt.execute_test(Thresholds)
    # print('Threshold')
