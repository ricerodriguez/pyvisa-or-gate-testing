
'''
This class is for interfacing with Ian's relay board
'''

import serial
from time import sleep
import serial.tools.list_ports



class relaySetup:
    #maybe make this an innit?
        def find_arduino(serial_number):
            for pinfo in serial.tools.list_ports.comports():
                if pinfo.serial_number == serial_number:
                    print(serial.Serial(pinfo.device))
                    return serial.Serial(pinfo.device)
                    raise IOError("Could not find an arduino - is it plugged in?")

        def test_cases(r):
            ser.reset_input_buffer()
            wo = 't' +str(r)
            ser.write(wo.encode('utf-8'))
            ser.readline()

        def relay(i):
            ser.reset_input_buffer()
            s='s'+str(i)
            ser.write(s.encode('utf-8'))
            ser.readline()

        def read_inputs():
            ser.reset_input_buffer()
            sleep(.05)
            ser.write('o'.encode('utf-8'))
            sleep(.05)
            c = ser.read(4)
            ser.readline()
            return c

        def Multirelay(i):
            ser.reset_input_buffer()
            s='*'+str(i)
            ser.write(s.encode('utf-8'))
            ser.readline()
