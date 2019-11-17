#!/usr/bin/env python
'''

Description:
    The voltage threshold test determines the minimum input Voltage
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
__author__ = "Victoria Rodriguez"
__credits__ = "Isaac Morales"
__email__ = "rice.rodriguez@ttu.edu"
__status__ = "Prototype"


import pyvisa
import logging
import argparse as arg
from resources import SMUSetup, DMMSetup
from time import sleep

'''
VoltageThresholdTest class is not meant to be called by anything other than the
VoltageThresholdTestHigh and VoltageThresholdTestLow classes. They do not share an
inheritance. This is done so that the user_interface module can call on the high
and low classes without needing to instantiate the VoltageThresholdTest class
'''

class VoltageThresholdTest:
    def get_valid_pins(pin_vals):
        return [f'pin {i+1}' for i,pin in enumerate(pin_vals) if pin == 'IN']

    def __init__(self, vcc, pin_vals,mode):
        self.rm = pyvisa.ResourceManager()
        self.vcc = vcc
        self.msg = 'Please make sure you connected one input pin and one output pin'
        self.smu_setup = SMUSetup('volt', vcc if mode else 0 ,'volt')
        self.smu = self.smu_setup.smu
        
        # Write the DMM Setup class once we figure out what the alias is
        self.dmm_setup = DMMSetup('volt')
        self.dmm = self.dmm_setup.dmm

        self.outcomes = dict.fromkeys(VoltageThresholdTest.get_valid_pins(pin_vals))
        self.meas = dict.fromkeys(VoltageThresholdTest.get_valid_pins(pin_vals))


class VoltageThresholdTestHigh:
    def __init__(self,vcc,pin_vals):
        vt = VoltageThresholdTest(vcc,pin_vals,True)
        self.rm = vt.rm
        self.msg = vt.msg
        self.smu_setup = vt.smu_setup
        self.smu = vt.smu

        self.dmm_setup = vt.dmm_setup
        self.dmm = vt.dmm

        self.vcc = vt.vcc
        self.outcomes = vt.outcomes
        self.meas = vt.meas

    def execute_test(self,pin,last=False):
        # Set voltage to VCC, then increase in steps until output reads 2
        self.smu.write('outp on')
        self.smu.write(f'form:elem volt')
        
        # DMM read
        out_val = float(self.dmm.query('meas:volt?'))
        sleep(0.5)
        res = self.vcc
        # Not sure if this should be 2 or not
        while out_val > 2:
            res -= 0.1
            # Set the level of the source
            self.smu.write(f'sour:volt:lev {res}')
            out_val = float(self.dmm.query('meas:volt?'))

        if last:
            self.smu.write('*rst;outp off;*cls')
            self.dmm.write('*rst;outp off;*cls')
            self.rm.close()

        self.meas[pin] = res
        return res

class VoltageThresholdTestLow:
    def __init__(self,vcc,pin_vals):
        vt = VoltageThresholdTest(vcc,pin_vals,False)
        self.rm = vt.rm
        self.msg = vt.msg
        self.smu_setup = vt.smu_setup
        self.smu = vt.smu

        self.dmm_setup = vt.dmm_setup
        self.dmm = vt.dmm

        self.vcc = vt.vcc
        self.outcomes = vt.outcomes
        self.meas = vt.meas

    def execute_test(self,pin,last=False):
        # Set voltage to VCC, then increase in steps until output reads 2
        self.smu.write('outp on')
        self.smu.write(f'form:elem volt')
        
        # DMM read
        out_val = float(self.dmm.query('meas:volt?'))
        sleep(0.5)
        res = self.vcc
        # Not sure if this should be 2 or not
        while out_val < 2:
            res += 0.1
            # Set the level of the source
            self.smu.write(f'sour:volt:lev {res}')
            out_val = float(self.dmm.query('meas:volt?'))

        if last:
            self.smu.write('*rst;outp off;*cls')
            self.dmm.write('*rst;outp off;*cls')
            self.rm.close()

        self.meas[pin] = res
        return res
    


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

    # Vcc = int(input('What is the Vcc of your device? \n'))
    # pinStart = bool(input('Are starting with an output of 1 or 0? \n'))



    # vt = VoltageThreshold(relay,range(1,14))
    # vt.execute_test(Vcc,pinStart)

    # vt = VoltageThresholdTest(['IN','OUT','IN','OUT','VCC','IN','OUT','IN','OUT','GND']).VoltageThresholdHigh(['IN','OUT','IN','OUT','VCC','IN','OUT','IN','OUT','GND'])

    vth = VoltageThresholdTestHigh(5,['IN','OUT','IN','OUT','VCC','IN','OUT','IN','OUT','GND'])
