#!/usr/bin/env python
'''
Description: The output drive current test verifies that
             the output voltage is maintained for a specified
             drive current.

Procedure
  1. Configure the device so that the output pin under test
     will be in a logic-level LOW state.
  2. Force the voltage level on the output pin under test
     to be 0.40 VDC.
  3. Measure the current draw IOL from the output pin
     under test.
  4. Configure the device so that the output pin under test
     will be in a logic-level HIGH state.
  5. Force the voltage level on the output pin under
     test to be 2.40 VDC.
  6. Measure the current draw IOH from the output pin under test.

Pass:
  IOH >= 2.10 mA and IOL >= -1.00 mA
'''
__author__ = "Victoria (Rice) Rodriguez"
__email__ = "rice.rodriguez@ttu.edu"
__status__ = "Prototype"
import pyvisa
import logging
from resources import SMUSetup
    
class OutputDriveCurrentTest:
    def get_valid_pins(pin_vals):
        return [f'pin {i+1}' for i,pin in enumerate(pin_vals) if pin == 'OUT']

    def __init__(self,rm,vcc,pin_vals):
        self.rm = rm
        self.instr = SMUSetup(src='volt',lev='0.40',sens='curr',rm=self.rm)
        self.smu = self.instr.smu
        self.meas = dict.fromkeys(OutputDriveCurrentTest.get_valid_pins(pin_vals))
        self.outcomes = dict.fromkeys(OutputDriveCurrentTest.get_valid_pins(pin_vals))
        self.hi = OutputDriveCurrentTestHigh(self.meas,self.outcomes)
        self.lo = OutputDriveCurrentTestLow(self.meas,self.outcomes)

    def execute_test(self,pin,mode,last=False):
        if mode.upper() == 'HIGH':
            self.instr.setup(src='volt',lev='2.4',sens='curr')
        else:
            self.instr.setup(src='volt',lev='0.4',sens='curr')
        self.smu.write('outp on')
        self.smu.write('form:elem curr')
        res = self.smu.query('read?')
        fres = float(f'{float(res):.3f}')
        self.meas[pin] = fres
        self.outcomes[pin] = (fres >= 0.0021) if mode.upper() == 'HIGH' else (fres >= -0.001)
        if last:
            self.smu.write('*rst;outp off;*cls')
            # self.rm.close()
        if mode.upper() == 'HIGH':
            self.hi.meas = self.meas
            self.hi.outcomes = self.outcomes
            return self.hi
        elif mode.upper() == 'LOW':
            self.lo.meas = self.meas
            self.lo.outcomes = self.outcomes
            return self.lo

        else: return self

class OutputDriveCurrentTestHigh:
    get_valid_pins = OutputDriveCurrentTest.get_valid_pins
    def __init__(self,meas,outcomes):
        self.meas = meas
        self.outcomes = outcomes

class OutputDriveCurrentTestLow:
    get_valid_pins = OutputDriveCurrentTest.get_valid_pins
    def __init__(self,meas,outcomes):
        self.meas = meas
        self.outcomes = outcomes
