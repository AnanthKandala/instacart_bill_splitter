from lxml import html
import pandas as pd
import re
import os
import json

# Function to parse the html receipt and return a dataframe with the receipt information
def parse_html_receipt(html_path):

    #check if html_path exists
    if not os.path.exists(html_path):
        raise ValueError(f'html_path: {html_path} does not exist')
    # Read the local HTML file
    with open(html_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    images_dir = f"{re.sub('.html', '', html_path)}_files"

    # Parse the HTML content using lxml
    parsed_html_receipt = html.fromstring(file_content)

    # Extract all class attributes from the HTML elements
    class_attributes = parsed_html_receipt.xpath('//@class')

    # obtain unique kinds of delivered items
    delivered_item_tags = []
    for cls in class_attributes:
        if 'item-row item-delivered' in cls:
            if cls not in delivered_item_tags:
                delivered_item_tags.append(cls)

    # Create a dictionary to store the information of the delivered items        
    items_dict = {'item-name':[],  'item-price':[], 'item-image':[]}
    for delivered_item_tag in delivered_item_tags:
        div_element = parsed_html_receipt.xpath(f'.//div[@class="{delivered_item_tag}"]')
        # Obtain all subelements inside the div element
        for item_div in div_element:
            # print(html.tostring(item_div, encoding='unicode'))
            for class_name in items_dict.keys():
                if class_name == 'item-name': #obtain item name
                    item_name =  item_div.xpath(f'.//div[@class="{class_name}"]')
                    cleaned_text = [div.text_content().replace('\n', '') for div in item_name ]
                    items_dict[class_name].append(cleaned_text[0])
                if class_name == 'item-price': #obtain item price
                    div_elements = item_div.xpath(f'.//div[@class="{class_name}"]')
                    cleaned_prices = [div.text_content().replace('\n', '') for div in div_elements]
                    # print(cleaned_prices)
                    items_dict[class_name].append(float(re.search(r'Final item price:\$(\d+\.\d+)', cleaned_prices[0]).group(1)))
                if class_name == 'item-image': #obtain the image of the item  
                    div_elements = item_div.xpath('.//div[@class="item-image"]/img/@src').pop().split('/')[-1]
                    image_location = f'{images_dir}/{div_elements}'
                    items_dict[class_name].append(image_location)
            
    delivered_items_df = pd.DataFrame(items_dict) #DataFrame with the delivered items

    # Obtain the total price of the order and miscellaneous charges
    misc_charges = {'charge-type':[], 'amount':[]}
    charge_type = parsed_html_receipt.xpath('.//td[@class="charge-type"]/text()') #extract the charges
    amount_type = parsed_html_receipt.xpath('.//td[@class="amount"]/text()') #extract the cost for each charge
    misc_charges['charge-type'] = [c for c in charge_type if c!='Instacart+ Member Free Delivery!'] #remove the free delivery charge
    misc_charges['amount'] = [float(i.replace('$', '')) for i in amount_type]
    misc_charges_df = pd.DataFrame(misc_charges) #DataFrame with the miscellaneous charges


    #obtain the delivery details
    delivery_details = parsed_html_receipt.xpath('//div[@class="DriverDeliverySchedule"]/text()') #extract the charges
    delivery_string = delivery_details[0].replace('\n', '')

    #obtain the payment details
    div_element = parsed_html_receipt.xpath(f'.//div[@class="credit-card"]')
    payment_string = str(div_element[0].text_content())
    pattern = r'\d{4}'
    match = re.search(pattern, payment_string)
    assert match, 'No credit card number found.'
    credit_card = match.group()
    with open('credit_cards.json', 'r') as f:
        stored_credit_cards = json.load(f)
    creditor = stored_credit_cards[str(credit_card)]
    payment_string = f'{payment_string} : {creditor}'
    print(payment_string)

    #obtain the expense title to be uploaded to splitwise
    div_element = parsed_html_receipt.xpath(f'.//div[@class="DriverDeliverySchedule"]')
    delivery_string = str(div_element[0].text_content())
    regex = r'Your order from (\w+) was placed on (\w+ \d{1,2}[a-z]{2}, \d{4}) and delivered on (\w+ \d{1,2}[a-z]{2}, \d{4})'
    match = re.search(regex, delivery_string)
    store_name = match.group(1)
    delivery_date = match.group(3)
    expense_title = f"{store_name}: {delivery_date}"
    print(expense_title)

    return delivered_items_df, misc_charges_df, delivery_string, payment_string, expense_title, creditor