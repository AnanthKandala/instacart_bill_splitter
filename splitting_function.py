import panel as pn
import numpy as np
import pandas as pd


def split_function(self):
    #creating a dataframe to store the split charges
    self.split_bill = self.delivered_items_widget.value.copy()
    for person in self.people + ['all']: #adding columns for each person and a column for all
        self.split_bill[person] = [np.nan]*len(self.split_bill)

    #populating the dataframe with the split charges based off the buttons pressed
    for index, item in self.delivered_items_widget.value.iterrows():
        if self.all_buttons[index].value == ['all']: #every one is involved in the expense
            for person in self.people:
                self.split_bill.loc[index, person] = item['item-price']/len(self.people)
                self.split_bill.loc[index, 'all'] = 'yes'
        else:
            people_in_expense = self.selection_widget[index].value
            if len(people_in_expense) != 0: #atleast one person is involved in the expense
                self.split_bill.loc[index, 'all'] = 'no'
                for person in self.people:
                    if person in people_in_expense:
                        self.split_bill.loc[index, person] = item['item-price']/len(people_in_expense)
                    else:
                        self.split_bill.loc[index, person] = 0

    print(self.split_bill)

    #checking if all expenses have been split
    split_status = self.split_bill.isnull().values.any()
    if split_status:
        display_string = '***Please select people involved in each expense'
    else:
        #calculate the total amount spent by each person
        def get_charge(charge_name, dataframe):
            try:
                return dataframe[dataframe['charge-type'].str.lower()==charge_name.lower()]['amount'].values[0]
            except:
                print(dataframe)
                return

        sub_total = get_charge('Items Subtotal', self.misc_charges_widget.value) #total amount spent on items excluding taxes and tips
        total_charge = get_charge('Total', self.misc_charges_widget.value) #total amount spend that includes taxes and tips
        individual_charges = {person: sum(self.split_bill[person]) for person in self.people} #total amount spent by each person
        assert np.isclose(sub_total, sum(individual_charges.values())), 'Subtotal does not match the sum of individual charges'
        self.split_charges = {key:round(value, 2) for key, value in individual_charges.items()} #rounding off the charges to two decimal places
        print(f'Total charged: ${total_charge}')
        print(f'Total amount spent on items: ${sub_total}')
        print(f'Individual charges: {self.split_charges}')
        self.terminal.write(f'Total charged: ${total_charge}\n')
        self.terminal.write(f'Total amount spent on items: ${sub_total}\n')
        self.terminal.write(f'Individual charges: {self.split_charges}\n')

        display_string = 'All expenses have been split'
    self.terminal.write(f'Split button pressed!: \n{display_string}\n')
    print(f'Split button pressed!: {display_string}\n')
