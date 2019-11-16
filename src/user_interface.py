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
import PySimpleGUI as gui
from . import *
from resources import RelayBoard
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
                chip.output_sc_test()
            elif test == 'output drive current test':
                chip.output_dc_test()
            elif test == 'functional test':
                chip.functional_test()
            elif test == 'voltage threshold test':
                chip.voltage_threshold_test()
            else:
                continue

# Contains the dataset for the individual chip
class ICDataset:
    def __init__(self,num,pins):
        logging.debug('Created a new IC dataset object reference, number %(num)s')
        # List of what the pins are
        self.pins = pins
        # Which chip in the set
        self.num = num
        # References to the subclasses
        self.refs = {}
        self.relay_board = RelayBoard()

    def contact_test(self):
        logging.debug('Beginning the Contact Test')
        gui.PopupOK('Please move the yellow header to VCC and GND')
        con = ContactTest()
        # Add the object reference to the dict so we have access to it
        self.refs['contact'] = con
        # On all pins except VCC and GND
        for pin in [i for i,pin in enumerate(self.pins) if pin != 'VCC' and pin != 'GND']:
            self.relay_board.set_relay(pin)
            con.execute_test_pin()
            # self.contact_res.append(con.execute_test_pin())
            
        logging.info('Contact Test Results: {}'.format(pprint.pformat(self.contact_res)))

    def power_consumption_test(self):
        logging.debug('Beginning the Power Consumption Test')
        pctest = PowerConsumptionTest(5)
        self.refs['power consumption'] = pctest


def start_tests(pin_vals,tests):
    tab_layout = [[gui.Image('resources/placeholder.png')]]
    hist_layout = [gui.TabGroup([[gui.Tab(title=test,
                                          layout=[[gui.Image('resources/placeholder.png')]],
                                          key='tab {}'.format(test))] for test in tests])]
    # print(pprint.pformat(hist_layout))
    layout2 = [[gui.T('Testing')],
               hist_layout]
    win = gui.Window('Test',layout2)
    event,val=win.read(timeout=10)
    # Start by making the overarching dataset class

    chip_set = TotalDataset(tests)
    chip_count = 1
    while True:
        chip = ICDataset(chip_count,pin_vals)
        chip_set.run_tests(chip)
        
    return


if __name__ == '__main__':
    started=False
    w_max,h_max=80,100
    off=2
    left_pins = gui.Column(list(([gui.T('PIN {}'.format(i+1),key='pin_{}'.format(i+1),visible=False),
                                  gui.Combo(default_value='Select',values=('VCC','GND','IN','OUT'),font=('Helvetica',14),key=('left_{}'.format(i+1)),auto_size_text=True,visible=False)] for i in range(8))),key='left_pins')
    right_pins = gui.Column(list(([gui.T('PIN {}'.format(i+9),key='pin_{}'.format(i+9),visible=False),
                                   gui.Combo(default_value='Select',values=('VCC','GND','IN','OUT'),font=('Helvetica',14),key=('right_{}'.format(i+1)),auto_size_text=True,visible=False)] for i in range(8))),key='right_pins')
    # test_boxes = [[gui.Checkbox(text = test,justification='left'),gui.Checkbox(text=LIST_TESTS[i+3],justification='right')] for (i,test) in enumerate(LIST_TESTS) if i<3]
    test_boxes = [[gui.Column(list([gui.Checkbox(text=test,key=test.lower())] for (i,test) in enumerate(LIST_TESTS) if i<3)),
                   gui.Column(list([gui.Checkbox(text=test,key=test.lower())]) for (i,test) in enumerate(LIST_TESTS) if i>=3)]]
    frame_tests = gui.Frame('Select Tests',test_boxes,key='tests')

    path_names = [[gui.T('Dataset')],
                  [gui.Input(key='fname_data_input'),gui.FileSaveAs()],
                  [gui.T('Histograms')],
                  [gui.Input(key='fname_hist_input'),gui.FolderBrowse()]]
    frame_paths = gui.Frame('Options',path_names)
    layout = [[gui.Text('Chip Test',font=('Helvetica',20))],
              [gui.Button('Close')],
              [gui.Slider(range=(4,16),default_value=16,resolution=2,disable_number_display=False,key='num_pins',tooltip='Set number of pins on the chip',orientation='h')],
              [left_pins,gui.Graph(canvas_size=(2*w_max,2*h_max),graph_bottom_left=(-w_max-off,-h_max-off),graph_top_right=(w_max+off,h_max+off),key='chip'),right_pins],
              [frame_tests],
              [frame_paths],
              [gui.Button('Start Tests')]]


    winit=gui.Window('Main',layout).Finalize()
    event,val = winit.Read(timeout=10)
    wcurr = winit
    graph = wcurr['chip']
    while True:
        event,val = wcurr.Read(timeout=10)
        graph.Erase()
        # chip=graph.DrawRectangle(top_left=(-w,h),bottom_right=(w,-h),fill_color='gray',line_color='black')
        rows = int(val['num_pins']/2)
        w,h=w_max,(rows/8)*h_max
        arc_points = [int(.15*w),int(.8*h_max)]
        # graph.draw_line((-w,-h),(-w,h),color='black')
        graph.draw_line((-w,h_max),(-arc_points[0],h_max),color='black')
        arc=graph.draw_arc((-arc_points[0],h_max),(arc_points[0],arc_points[1]),arc_color='black',extent=-180,start_angle=0,style='arc')
        graph.draw_line((arc_points[0],h_max),(w,h_max),color='black')
        graph.draw_line((w,h_max),(w,-h))
        graph.draw_line((w,-h),(-w,-h))
        graph.draw_line((-w,-h),(-w,h_max))

        for i in range (8):
            wcurr['left_pins'].Rows[i][0].update(visible=(i+1<=rows))
            wcurr['left_pins'].Rows[i][1].update(visible=(i+1<=rows))
            wcurr['pin_{}'.format(i+9)].update(value='PIN {}'.format(rows+1+i))
            wcurr['right_pins'].Rows[i][0].update(visible=(i+1<=rows))
            wcurr['right_pins'].Rows[i][1].update(visible=(i+1<=rows))

        if event == 'Close':
            print(pprint.pformat(winit['left_pins'].__dict__))
            # print(pprint.pformat(val))
            break

        elif event == 'Start Tests':
            pin_vals = winit['left_pins'].ReturnValuesList[:rows]+winit['right_pins'].ReturnValuesList[:rows]
            tests = [test for test,v in val.items() if v is True]
            # print(pprint.pformat(winit['tests'].Rows[1][1].__dict__))
            if '' in pin_vals:
                msg = 'Undefined value for pin {}'.format(1+pin_vals.index(''))
                logging.error(msg)
                gui.PopupError(msg)
            # Change to elif after finished debugging
            elif not started:
                wcurr.close()
                start_tests(pin_vals,tests)
            break