import panel as pn
import numpy as np
import pandas as pd
import os
import sys

#importing custom functions
from inputs import add_input_buttons
from upload_html import upload_and_parse
from app import App

if __name__ == '__main__':
    app = App()
    print('Starting the server')
    pn.serve(app.template, port=5006)




