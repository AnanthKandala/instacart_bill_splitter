import panel as pn
import numpy as np
import pandas as pd
import random

def random_selections(self):
    delivered_items_df = self.delivered_items_widget.value.copy()
    num_people = len(self.people)
    def random_bool(p):
        return random.random() < p
    for person in self.people:
        delivered_items_df[person] = [random_bool(0.5) for i in range(len(delivered_items_df))]

    #generate 6 random integers between 0 and len(delivered_items_df)
    import numpy as np
    random_indices = np.random.randint(0, len(delivered_items_df), size=7)
    for person in self.people:
        for j in random_indices:
            delivered_items_df.at[j, person] = False
    delivered_items_df['all'] = [True]*len(delivered_items_df)
    # for j in random_indices:
    #     delivered_items_df.at[j, f'all'] = True

    print(delivered_items_df)
    for index, item in delivered_items_df.iterrows():
        # print(self.template.main[0][1])
        row = self.template.main[0][1][index][0]
        if item['all'] == True:
            row[4].value = []
            row[5].value = ['all']
        else:
            row[4].value = item[item==True].index.values.tolist()
            row[5].value = []
        