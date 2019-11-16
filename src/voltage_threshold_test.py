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

Outcomes:
    Vil:
        Passing Condition: Vil >= .8 VDC
        Failing Condition: Vil < .8 VDC
    Vih:
        Passing Condition: Vih <= 2 VDC
        Failing Condition: Vih > 2 VDC

'''
__author__ = "Isaac Morales"
__email__ = "isaac.morales@ttu.edu"
__status__ = "Prototype"


import pyvisa
import logging
import argparse as arg
from resources import SMUSetup, RelayBoard
from time import sleep

class VoltageThreshold:
    def __init__(self, relay, pins):
        self.rm = pyvisa.ResourceManager()
        self.msg = 'Please make sure you connected one input pin and one output pin'
        self.instr = SMUSetup('volt', 0 ,'volt')
        self.smu = self.instr.smu
        self.res = None
        self.outcome = None
        self.relay = relay
        self.pins = pins
        self.meas = {}

    def execute_test(self, Vcc, pinStart):

        # 9225 for a
        # 18450 for b
        # self.relay.multirelay(pinPos)
        thresh = 0

        for currPin in self.pins:
            #for each step up or down
            #stepping down
            logging.warning('on pin number: {}'.format(currPin))
            if pinStart:
                start = Vcc * 10
                finish = -1
                step = -1
                # readOut = 0
                compare = 20 # Vih
                #stepping up
                logging.warning('starting at vcc, going down by .1')
            else:
                start = 0
                finish = Vcc * 10 + 1
                step = 1
                compare = 8 # Vil
                logging.warning('starting at 0, going down up .1')
            for volts in range(start, finish, step):
                logging.warning('current volage level:{}'.format(volts))
                #write the new voltage to the input pin we're working with
                self.instr.setup('volt', volts/10, 'curr')
                self.smu.write('outp on')
                #wait a bit before reading the result at the output
                time.sleep(.025)
                    #make sure we read it as a binary value
                read = int(self.relay.read_inputs(), base = 2)
                print(volts,read)
                    #we may need to mask later? idk rn but if we're no longer
                    #seeing the same output, that means we hit a threshold.
                if read != pinStart and thresh == 0:
                    thresh = volts
                    self.rm.close() #make sure you're closing this shit!
                        #if we are stepping down and our threshold passed
                    if pinStart and volts <= compare:
                        self.outcome = True #then the test was successful, we passed
                        # self.rm.close()
                        self.meas['pin {}'.format(currPin)][1] = thresh   #return the threshold for this OR gate
                        #if we are stepping up and our threshold passed
                    elif not pinStart and volts > compare:
                        self.outcome = True #then the test was successful, we passed
                        # self.rm.close()
                        self.meas['pin {}'.format(currPin)][0] = thresh  #return the threshold for this OR gate
                    else: #otherwise the test failed, we failed :\
                        self.outcome = False
                        # self.rm.close()
                        self.meas['pin {}'.foramt(currPin)] = thresh, thresh
                else:
                    self.smu.write('*rst;outp off;*cls;')


        self.rm.close()


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

    Vcc = int(input('What is the Vcc of your device? \n'))
    pinStart = bool(input('Are starting with an output of 1 or 0? \n'))



    relay = RelayBoard()
    vt = VoltageThreshold(relay,range(1,14))
    vt.execute_test(Vcc,pinStart)
    # print('Threshold')
