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
    def __init__(self, relay):
        self.rm = pyvisa.ResourceManager()
        self.msg = 'Please make sure you connected one input pin and one output pin'
        self.instr = SMUSetup('volt', 0 ,'volt')
        self.smu = self.instr.smu
        self.res = None

        self.relay = relay


    def execute_test(self, Vcc, pinStart):

        # 9225 for a
        # 18450 for b
        # self.relay.multirelay(pinPos)
        thresh_0, thresh_1, thresh_2, thresh_3 = 0
        if pinStart:
            start = Vcc * 10 + 1
            finish = 0
            step = -1
            # readOut = 0
        else:
            start = 0
            finish = Vcc * 10 + 1
            step = 1
            # readOut = 1

            #for each step up or down
        for volts in range(start, finish, step):
            #write the new voltage to the input pin we're working with
            self.smu.setup('volt', volts/10, 'curr')
            self.smu.write('outp on')
            #wait a bit before reading the result at the output
            sleep(.025)
                #make sure we read it as a binary value
            read = int(self.relay.read_inputs(), base = 2)
            print(volts,read)
                #we may need to mask later? idk rn
            if read != pinStart and thresh_0 == 0:
                thresh = volts


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




    vt = VoltageThreshold()
    Thresholds =  vt.execute_test(Vcc,pinStart)
    vt.execute_test(Thresholds)
    # print('Threshold')
