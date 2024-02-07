import panel as pn
import param

def add_input_buttons(self):

    template = self.template
    Input = {}
    w0 = 220
    Input['people'] = pn.widgets.TextInput(value='  ', name='people', width=w0) #list the people involved in the expense
    Input['upload'] = pn.widgets.Button(name='Upload!', width=w0)
    Input['split']  = pn.widgets.Button(name='Split!', width=w0)
    Input['splitwise'] = pn.widgets.Button(name='Upload to Splitwise!', width=w0)
    #input html receipt to parse, accept only html files
    Input['file_input'] = pn.widgets.FileInput( accept='.html', name='HTML receipt', width=w0)

    inputs = ['people', 'file_input', 'upload', 'split', 'splitwise']
    for item in inputs:
        template.sidebar.append(Input[f'{item}'])
    template.sidebar.append(pn.Column()) #for comments/errors
    #adding a terminal to print outputs
    terminal = pn.widgets.Terminal(options={"cursorBlink": True}, height=300, sizing_mode="stretch_width")
    self.terminal = terminal
    template.sidebar.append(terminal)

    #uploading, parsing and populating the panel interface with buttons
    print('Input buttons added to the template')
    self.terminal.write('Input buttons added to the template\n')
    return Input