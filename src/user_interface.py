#!/usr/bin/env python
'''
Description: Allows the user to interface with all of the tests:
  1. Contact Test
  2. Power Consumption Test
  3. Output Short Current Test
  4. Output Drive Current Test
  5. Functional Test
  6. Voltage Threshold Test
'''
__author__ = "Victoria (Rice) Rodriguez"
__email__ = "rice.rodriguez@ttu.edu"
__status__ = "Prototype"

import logging
import argparse
import pprint
import re
import PySimpleGUI as gui
# from . import *
from statistics import mean
from contact_test import ContactTest
from power_consumption_test import PowerConsumptionTest
from output_short_current_test import OutputShortCurrentTest
from voltage_threshold_test import VoltageThresholdTest
# from resources import RelayBoard
LIST_TESTS = ['Contact Test','Power Consumption Test','Voltage Threshold Test','Output Short Current Test','Output Drive Current Test','Functional Test']
class TotalDataset:
    def __init__(self,tests):
        logging.debug('Created a new total dataset reference.')
        self.tests = tests
        self.chips = []
        self.sum_ct = []
        self.Cpk = None

    def add_chip(self,chip):
        self.chips.append(chip)

    def run_tests(self,chip):
        # Go through all the tests
        for test in self.tests:
            if test == 'contact test':
                chip.contact_test()
            elif test == 'power consumption test':
                chip.power_consumption_test()
            elif test == 'output short current test':
                chip.output_short_current_test()
            elif test == 'output drive current test':
                chip.output_drive_current_test()
            elif test == 'functional test':
                # chip.functional_test()
                pass
            elif test == 'voltage threshold test':
                chip.voltage_threshold_test()
            else:
                continue

# Contains the dataset for the individual chip
class ICDataset:
    def __init__(self,num,pins,vcc):
        logging.debug('Created a new IC dataset object reference, number %(num)s')
        # List of what the pins are
        self.pins = pins
        # Which chip in the set
        self.num = num
        # References to the subclasses
        self.refs = {}
        # VCC level
        self.vcc = vcc

    def contact_test(self):
        logging.debug('Beginning the Contact Test')
        valid_pins = ContactTest.get_valid_pins(self.pins)
        con = ContactTest(self.pins)
        # Add the object reference to the dict so we have access to it
        self.refs['contact test'] = con

        # Get list of input pins
        input_pins = (i+1 for i,pin in enumerate(self.pins) if pin == 'IN')
        # Tell user which pins to set to GND
        try:
            input_pins[-1] = f'and {input_pins[-1]}'
            msg = f'Please set pins {", ".join(input_pins)} to GND.'
            gui.Popup(msg,title='Contact Test')
        except TypeError:
            msg = f'Please set pin {input_pins} to GND.'
            gui.Popup(msg,title='Contact Test')

        # Go through list of pins
        for i,pin in enumerate(valid_pins):
            # self.relay_board.set_relay(pin)
            msg = f'Please move the SMU probe to pin {pin}.'
            gui.Popup(msg,title='Contact Test')
            con.execute_test_pin(pin,i==len(valid_pins)-1)

    def power_consumption_test(self):
        logging.debug('Beginning the Power Consumption Test')

        # Get list of output pins
        output_pins = (str(i+1) for i,pin in enumerate(self.pins) if pin == 'OUT')
        try:
            output_pins[-1] = f'and {output_pins[-1]}'
            msg = f'Please float output pins {", ".join(output_pins)}.'
            gui.Popup(msg,title='Power Consumption Test')
        except TypeError:
            msg = f'Please float output pin {output_pins}.'
            gui.Popup(msg,title='Power Consumption Test')
            # output_pins = [output_pins]

        pctest = PowerConsumptionTest(self.vcc,self.pin_vals)
        self.refs['power consumption test'] = pctest

        msg = 'Please move the SMU probe to the VCC pin {self.pins.index("VCC")+1}.'
        gui.Popup(msg,title='Power Consumption Test')
        # There's only one VCC pin
        pctest.execute_test(f'pin {self.pins.index("VCC")+1}',last=True)

    def output_short_current_test(self):
        logging.debug('Beginning the Output Short Current Test')
        gui.Popup('Set the input pins such that the DUT should output a logic HIGH.',title='Output Short Current Test')
        osct = OutputShortCurrentTest(self.pins)
        valid_pins = OutputShortCurrentTest.get_valid_pins(self.pins)
        for i,pin in enumerate(valid_pins):
            gui.Popup(f'Please move the probe from the SMU to {pin}.',title='Output Short Current Test')
            osct.execute_test(pin,i==len(valid_pins)-1)


    # There's definitely way better ways to do this but I don't have time
    def voltage_threshold_test(self):
        logging.debug('Beginning the Voltage Threshold Test')
        # Get list of input pins
        input_pins = [f'pin {i+1}' for i,pin in enumerate(self.pins) if pin == 'IN']
        vtl = VoltageThresholdLow(self.vcc,self.pins)

        for i,pin in enumerate(input_pins):
            gui.Popup(f'Move the probe of the SMU to input {pin} and set up the inputs so that the output pin should result in a logic level LOW while {pin} is also set to logic level LOW. Move the probe of the DMM to the output pin.',title='Voltage Threshold Test (Low)')
            vtl.execute_test(pin,i==len(input_pins)-1)

        vth = VoltageThresholdHigh(self.vcc,self.pins)
        for i,pin in enumerate(input_pins):
            gui.Popup(f'Move the probe of the SMU to input {pin} and set up the inputs so that the output pin should result in a logic level HIGH while {pin} is also set to logic level HIGH. Move the probe of the DMM to the output pin.',title='Voltage Threshold Test (High)')
            vth.execute_test(pin,i==len(input_pins)-1)
        

def start_tests(fname,pin_vals,tests,vcc):
    tab_layout = [[gui.Image('resources/placeholder.png')]]
    hist_layout = [gui.TabGroup([[gui.Tab(title=test,
                                          layout=[[gui.Image('resources/placeholder.png')]],
                                          key='tab {}'.format(test))] for test in tests])]
    layout2 = [[gui.T('Testing')],
               hist_layout]
    win = gui.Window('Test',layout2)
    event,val=win.read(timeout=10)
    # Make the list of pins
    list_pins = ['pin {}'.format(i) for i in range(1,len(pin_vals)+1)]
    # Start by making the overarching dataset class
    chip_set = TotalDataset(tests)
    chip_count = 1

    if 'voltage threshold test' in tests:
       tests[tests.index('voltage threshold test')] = 'voltage threshold test low'
       tests.append('voltage threshold test high')
    print(tests)
    while True:
        chip = ICDataset(chip_count,pin_vals,vcc)
        chip_set.add_chip(chip)
        chip_set.run_tests(chip)
        answer=gui.PopupYesNo('Tests finished for chip #{}. Do you want to test another chip?'.format(chip_count))
        if answer=='Yes':
            chip_count+=1
            continue
        else:
            # Done collecting data
            # Get all the averages
            averages = {t:{p:mean((c.refs[t].meas[p] for c in chip_set.chips)) for p in eval(t.title().replace(' ','')).get_valid_pins(pin_vals)} for t in tests}
            with open(fname,'w+') as f:
                for t in tests:
                    f.write(f'{t.upper():~^50}\n')
                    for p in eval(t.title().replace(' ','')).get_valid_pins(pin_vals):
                        f.write(f'{p.upper()} AVERAGE = {averages[t][p]}\n')

            break
    return


if __name__ == '__main__':
    started=False
    loaded = False
    w_max,h_max=80,100
    off=2
    offset = 265
    max_pins=16
    pin_choices = ('VCC','GND','IN','OUT')
    test_boxes = [[gui.Column(list([gui.Checkbox(text=test,key=test.lower())] for (i,test) in enumerate(LIST_TESTS) if i<2)),
                   gui.Sizer(offset/2-25),
                   gui.Column(list([gui.Checkbox(text=test,key=test.lower())] for (i,test) in enumerate(LIST_TESTS) if i<4 and i >=2)),
                   gui.Sizer(offset/2-25),
                   gui.Column(list([gui.Checkbox(text=test,key=test.lower())] for (i,test) in enumerate(LIST_TESTS) if i>=4))]]
    
    frame_tests = gui.Frame('Select Tests',test_boxes,key='tests')

    menu_layout = [['&File', ['&Open','&Save']]]

    col_dataset = gui.Column([[gui.T('Dataset')],
                             [gui.Input(key='fname_data_input'),gui.FileSaveAs()]])
    col_hist = gui.Column([[gui.T('Histograms')],
                          [gui.Input(key='fname_hist_input'),gui.FolderBrowse()]])

    path_names = [[col_dataset,col_hist]]

    chip_layout = [[gui.Sizer(offset),
                    gui.Column(list(([gui.T('PIN {}'.format(i+1),key='pin_{}'.format(i+1),visible=False),
                                      gui.Combo(default_value='Select',
                                                values=pin_choices,
                                                font=('Helvetica',14),
                                                key=(f'left_{i+1}'),
                                                auto_size_text=True,visible=False)] for i in range(8))),
                               key='left_pins'),
                    gui.Graph(canvas_size=(2*w_max,2*h_max),
                              graph_bottom_left=(-w_max-off,-h_max-off),
                              graph_top_right=(w_max+off,h_max+off),
                              key='chip'),
                    gui.Column(list(([gui.T(f'PIN {max_pins-i}',key=f'pin_{max_pins-i}',visible=False),
                                      gui.Combo(default_value='Select',
                                                values=pin_choices,
                                                font=('Helvetica',14),
                                                key=(f'right_{i+1}'),
                                                auto_size_text=True,
                                                visible=False)] for i in range(8))),
                               key='right_pins'),
                    gui.Sizer(offset)],
                   [gui.T('VCC: '),gui.Spin(values=[i for i in range(1,12)],initial_value=5,tooltip='Set the voltage needed to send to the VCC pin to power the DUT.',key='vcc_lev')]]

    frame_chip = gui.Frame('Device Under Test', chip_layout)

                  
    frame_paths = gui.Frame('Options',path_names)
    layout = [[gui.Menu(menu_layout,key='menu')],
              [gui.Text('Chip Test',font=('Helvetica',20))],
              [gui.Slider(range=(4,16),
                          default_value=16,
                          resolution=2,
                          disable_number_display=False,
                          key='num_pins',
                          tooltip='Set number of pins on the chip',
                          orientation='h',
                          size=(84,20))],
              [frame_chip],
              [frame_tests],
              [frame_paths],
              [gui.Button('Close'),gui.Button('Start Tests')]]


    winit=gui.Window('Main',layout).Finalize()
    wcurr = winit
    graph = wcurr['chip']
    while True:
        event,val = wcurr.Read(timeout=10)
        graph.Erase()
        rows = int(val['num_pins']/2)
        w,h=w_max,(rows/8)*h_max
        arc_points = [int(.15*w),int(.8*h_max)]
        graph.draw_line((-w,h_max),(-arc_points[0],h_max),color='black')
        arc=graph.draw_arc((-arc_points[0],h_max),(arc_points[0],arc_points[1]),arc_color='black',extent=-180,start_angle=0,style='arc')
        graph.draw_line((arc_points[0],h_max),(w,h_max),color='black')
        graph.draw_line((w,h_max),(w,-h))
        graph.draw_line((w,-h),(-w,-h))
        graph.draw_line((-w,-h),(-w,h_max))

        event,val = wcurr.Read(timeout=100)
        rows = int(val['num_pins']/2)
        for i in range (8):
            wcurr['left_pins'].Rows[i][0].update(visible=(i+1<=rows))
            wcurr['left_pins'].Rows[i][1].update(visible=(i+1<=rows))
            wcurr['right_pins'].Rows[i][0].update(visible=(i+1<=rows),value=f'PIN {2*rows-i}')
            wcurr['right_pins'].Rows[i][1].update(visible=(i+1<=rows))

        if event == 'Close':
            break

        elif event == 'Start Tests':
            pin_vals = winit['left_pins'].ReturnValuesList[:rows]+winit['right_pins'].ReturnValuesList[rows-1::-1]
            tests = [test for test,v in val.items() if v is True]
            if '' in pin_vals:
                msg = 'Undefined value for pin {}'.format(1+pin_vals.index(''))
                logging.error(msg)
                gui.PopupError(msg)
            if not val['fname_data_input']:
                msg = 'Please select a filename to save the data to.'
                gui.PopupGetFile(message=msg,default_extension='.txt',save_as=True)
                
            # Change to elif after finished debugging
            elif not started:
                wcurr.close()
                started=True
                start_tests(val['fname_data_input'],pin_vals,tests,val['vcc_lev'])
            break

        elif event == 'Open':
            msg = 'Select a config file to open.'
            config=gui.PopupGetFile(message=msg)
            try:
                with open(config,'r') as f:
                    exec(f.read())
            except FileNotFoundError or TypeError:
                pass

        elif event == 'Save':
            msg = 'Choose a file to save configuration settings to.'
            config=gui.PopupGetFile(message=msg,default_extension='.config',save_as=True)
            try:
                with open(config,'w+') as f:
                    # updater = re.sub(r'\"((?:\bFalse\b)|(?:\bTrue\b)\"|(?:\d+(?:\.\d+)?))\"','\g<1>',
                    #                    '\n'.join([rf'wcurr["{key}"].update(value="{v}")' for key,v in val.items() if not v is None and not type(v) is tuple and not len(str(v))==0 and key!='menu']))
                    # f.write(f'loaded=True\n{updater}')
                    f.write(re.sub(r'\"((?:\bFalse\b)|(?:\bTrue\b)\"|(?:\d+(?:\.\d+)?))\"','\g<1>',
                                       '\n'.join([rf'wcurr["{key}"].update(value="{v}")' for key,v in val.items() if not v is None and not type(v) is tuple and not len(str(v))==0 and key!='menu'])))
                    
            except TypeError:
                pass

