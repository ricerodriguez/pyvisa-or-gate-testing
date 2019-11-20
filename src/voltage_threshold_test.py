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

    def __init__(self, rm, vcc, vih, vil, voh, vol, pin_vals):
        self.rm = rm
        self.msg = 'Please make sure you connected one input pin and one output pin'

        self.vcc = vcc
        self.vih = vih
        self.vil = vil
        self.voh = voh
        self.vol = vol
        
        self.smu_setup = SMUSetup(src='volt',lev='0',sens='volt',rm=rm)
        self.smu = self.smu_setup.smu
        
        # Write the DMM Setup class once we figure out what the alias is
        self.dmm_setup = DMMSetup('volt')
        self.dmm = self.dmm_setup.dmm

        self.outcomes = dict.fromkeys(VoltageThresholdTest.get_valid_pins(pin_vals))
        self.meas = dict.fromkeys(VoltageThresholdTest.get_valid_pins(pin_vals))
        self.hi = VoltageThresholdTestHigh(self.meas,self.outcomes)
        self.lo = VoltageThresholdTestLow(self.meas,self.outcomes)


    def execute_test(self,pin,mode,last=False):
        if mode.upper() == 'HIGH':
            self.smu_setup.setup(src='volt',lev=self.vcc,sens='volt')
        else:
            self.smu_setup.setup(src='volt',lev='0',sens='volt')
        
        # Set voltage to VCC, then increase in steps until output reads 2
        self.smu.write('outp on')
        self.smu.write(f'form:elem volt')
        
        # DMM read
        out_val = float(self.dmm.query('?'))
        sleep(0.5)
        res = self.vcc

        while out_val > self.vol if mode.upper() == 'HIGH' else out_val < self.voh:
            res = res - 0.1 if mode.upper() == 'HIGH' else res + 0.1
            if res > self.vcc or res < 0:
                out_val = float(self.dmm.query('?'))
                break
            # Set the level of the source
            self.smu.write(f'sour:volt:lev {res}')
            out_val = float(self.dmm.query('?'))

        fres = float(f'{float(res):.3f}')
        self.outcomes[pin] = (fres <= self.vih) if mode.upper() == 'HIGH' else (fres >= self.vil)
        self.meas[pin] = fres

        if mode.upper() == 'HIGH':
            self.hi.meas = self.meas
            self.hi.outcomes = self.outcomes
            return self.hi
        elif mode.upper() == 'LOW':
            self.lo.meas = self.meas
            self.lo.outcomes = self.outcomes
            return self.lo
        else:
            return self

        self.smu.write('*rst;outp off;*cls')
        return fres

class VoltageThresholdTestHigh:
    get_valid_pins = VoltageThresholdTest.get_valid_pins
    def __init__(self,meas,outcomes):
        self.meas = meas
        self.outcomes = outcomes

class VoltageThresholdTestLow:
    get_valid_pins = VoltageThresholdTest.get_valid_pins
    def __init__(self,meas,outcomes):
        self.meas = meas
        self.outcomes = outcomes
        
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


