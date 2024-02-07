import panel as pn
import pandas as pd
from html_parsing_function import parse_html_receipt
from functools import partial

#Parse the html receipt and return a dataframe with the receipt information and populate the panel template
def upload_and_parse(self):
    '''Gets triggered whenever the upload button is pressed. It uses the html_parsing function to obtain a dataframe of prices, and 
    populates the panel interface with the images, prices and buttons to select people involved. 
    *args = template, 
    '''
    template = self.template
    Input = self.Input
    template.main.clear()
    template.main.append(pn.Column(pn.Row(), pn.Row(), pn.Row())) #for the delivery string, items and charges and miscellanous charges
    People = Input['people'].value.split(',') #people involved in the transaction
    self.people = People
    html_path = Input['file_input'].filename
    #Obtain the DataFrames containing the items and misc charges using the html parsing functions
    delivered_items_df, misc_charges_df, delivery_string, payment_string, expense_title, creditor =  parse_html_receipt(html_path)#DataFrame containing the items
    #populate the panel objects with the DataFrames and the delivery string
    self.delivered_items_widget.value = delivered_items_df
    self.misc_charges_widget.value = misc_charges_df
    self.delivery_string_pane.object = delivery_string
    self.expense_title = expense_title
    self.creditor = creditor
    template.main[0][0] = pn.Column(pn.pane.Markdown(delivery_string), pn.pane.Markdown(payment_string)) #place the delivery string in the main template, row 0

    #place the items and charges in the main template, row 1
    column = pn.Column()
    selection_widget = {}
    all_buttons = {}
    m = 15
    align = 'center'
    def check_button_group(event, row, all_button):
        if len(all_button.value) == 0:
            row.disabled = False
        else:
            row.value = []
            row.disabled = True
        return
    
    def check_all_buttons_pressed(event, row, all_button):
        if len(row.value) == len(self.people):
            all_button.value = ['all']
        return

    #adding details of delivered item to the main template
    for index, item in delivered_items_df.iterrows():
        item_name = item['item-name']
        item_cost = item['item-price']
        item_image = item['item-image']
        item_index_pane = pn.pane.LaTeX(object=f'{index})', name='item_pane', width=5,margin=(m,m),align=align)
        item_name_pane = pn.pane.Markdown(object=f'{item_name}', name='item_pane', width=400,margin=(m,m),align=align)
        item_cost_pane = pn.pane.LaTeX(object=f'$\${item_cost}$', name='item_pane', width=50,margin=(m,m),align=align)
        selection_widget[index] = pn.widgets.CheckButtonGroup(name='', value=[], options=People,margin=(m,m),align=align)
        all_buttons[index] = pn.widgets.CheckButtonGroup(name='', value=[], options=['all'], margin=(m,m),align=align)
        all_buttons[index].param.watch(partial(check_button_group, row=selection_widget[index], all_button=all_buttons[index]), 'value')
        selection_widget[index].param.watch(partial(check_all_buttons_pressed, row=selection_widget[index], all_button=all_buttons[index]), 'value')
        h = item_cost_pane.height
        item_image_pane = pn.pane.Image(item_image, fixed_aspect=True, height=h)    
        #append everyhting to the main template
        column.append(pn.Column(pn.Row(item_index_pane, item_image_pane, item_name_pane, item_cost_pane, selection_widget[index], all_buttons[index]),pn.layout.Divider()))
        print(item_name, item_cost)
        # template.main.append(pn.Row(item_index_pane, item_name_pane, item_cost_pane, selection_widget[index]))
    self.selection_widget = selection_widget
    self.all_buttons = all_buttons
    template.main[0][1] = column

    #place the items and charges in the main template, row 2
    column = pn.Column()
    #adding details of miscellaneous charges to the main template
    for index, item in misc_charges_df.iterrows():
        item_name = item['charge-type']
        item_cost = item['amount']
        item_index_pane = pn.pane.LaTeX(object=f'{index})', name='item_pane', width=5,margin=(m,m),align=align)
        # item_image_pane = pn.pane.PNG(item_image, sizing_mode='scale_width')    
        item_name_pane = pn.pane.Markdown(object=f'{item_name}', name='item_pane', width=400,margin=(m,m),align=align)
        item_cost_pane = pn.pane.LaTeX(object=f'$\${item_cost}$', name='item_pane', width=50,margin=(m,m),align=align)
        column.append(pn.Column(pn.Row(item_index_pane, item_name_pane, item_cost_pane), pn.layout.Divider()))
        print(item_name, item_cost)
    template.main[0][2] = column
    self.terminal.write('Uploaded and parsed the html receipt\n')
    self.terminal.write(f"People involved are {' '.join(People)}\n")
    return