import panel as pn
import param
import numpy as np
import pandas as pd
import os
from functools import partial
import sys

#importing custom functions
from inputs import add_input_buttons
# from html_parsing_function import parse_html_receipt
from upload_html import upload_and_parse
from splitting_function import split_function
from pre_selected_frame import random_selections
from splitwise_function import create_expense

class App:
    def __init__(self):
        #initialize the panel interface
        pn.extension('katex', 'terminal')
        self.template = pn.template.BootstrapTemplate(title='Split thy bills!', sidebar_width=550)
        
        self.Input = add_input_buttons(self) #Adding input buttons to the template

        #initializing empty dataframes that will be populated when the upload button is pressed
        self.delivered_items_widget = pn.widgets.DataFrame()
        self.misc_charges_widget = pn.widgets.DataFrame()

        self.delivery_string_pane = pn.pane.Markdown('') #panel pane that holds the delivery string
        self.Input['upload'].param.watch(self.upload, 'value') #watch the upload button for changes
        self.Input['split'].param.watch(self.split_bill, 'value') #watch the split button for changes
        self.Input['splitwise'].param.watch(self.upload_to_splitwise, 'value') #watch the splitwise button for changes
        #payment details:

    def upload(self, *events):
        '''Gets triggered whenever the upload button is pressed. It uses the html_parsing function to obtain a dataframe of prices, and
        populates the panel interface with the images, prices and buttons to select people involved.'''
        upload_and_parse(self)
        random_selections(self) #randomly select people in the expense

    def split_bill(self, *events):
        '''Obtains the people involved in each expense and constructs a dataframe with the split charges'''
        split_function(self)

    def upload_to_splitwise(self, *events):
        '''Uploads the expenses to splitwise'''
        expense_Id = create_expense(self.split_charges, self.creditor, self.expense_title)
        self.terminal.write(f'Expense created: {self.expense_title}\n')
        self.terminal.write(f'Expense created: Id {expense_Id}\n')
        
    
    
