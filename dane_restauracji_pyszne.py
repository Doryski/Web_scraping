import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
start_time = time.time()

polish_signs = {'ę': 'e',
                'ł': 'l',
                'ó': 'o',
                'ś': 's',
                'ż': 'z',
                }

districts = []
page = requests.get('https://www.pyszne.pl/restauracja-warszawa')
soup = BeautifulSoup(page.content, 'html.parser')

for i in soup.find_all('div', class_='delarea')[1:]:
    i = i.get_text().lower()
    for letter in polish_signs.keys():
        i = i.replace(letter, polish_signs[letter])
    for sign in '()':
        i = i.replace(sign, '')
    i = i.split(' ')
    i = i[-1]
    districts.append(i)

pages_of_districts = []
for district in districts:
    pages_of_districts.append(
        f'https://www.pyszne.pl/restauracja-warszawa-{district}')

pages_of_codes = []
for site in pages_of_districts:
    page = requests.get(site)
    soup = BeautifulSoup(page.content, 'html.parser')
    for code in soup.find_all('div', class_='delarea'):
        code = code.get_text().split(' ')[0]
        pages_of_codes.append(f'{site}-{code}')
# 4240 pages to go through

names = []
kitchens = []
delivery_costs = []
min_order = []
districts = []
postal_codes = []

for site in range(len(pages_of_codes))[:]:  # done [:1000]
    district = pages_of_codes[site].split('-')[-3].capitalize()
    code = pages_of_codes[site][-6:]
    page = requests.get(pages_of_codes[site])
    soup = BeautifulSoup(page.content, 'html.parser')
    for i in soup.find_all('a', class_='restaurantname')[:-1]:
        i = i.get_text().strip()
        names.append(i)
        districts.append(district)
        postal_codes.append(code)

    for i in soup.find_all(class_='kitchens')[:-1]:
        i = i.get_text().strip()
        kitchens.append(i)

    for i in soup.find_all(class_='delivery-cost js-delivery-cost'):
        i = i.get_text().strip().replace('zł', '').replace(
            ',', '.').replace('GRATIS', '0.00').strip()
        delivery_costs.append(i)

    for div in soup.find_all('div', class_='delivery js-delivery-container'):
        if div.find('div', class_='min-order') is None:
            min_order.append('0.00')
        else:
            i = div.find('div', class_='min-order')
            i = i.get_text()[4:].replace('zł', '').replace(',', '.').strip()
            min_order.append(i)
    print(f"{site+1}/{len(pages_of_codes)}")


zippedList = list(zip(names, districts, postal_codes, kitchens,
                      delivery_costs, min_order))

# create initial .csv file
# df = pd.DataFrame(zippedList,
#                   columns=['Name', 'District', 'Postal code', 'Kitchens',
#                            'Delivery cost (PLN)', 'Min order cost (PLN)'])
# df = df.drop_duplicates(subset=['Name', 'District', 'Kitchens',
#                                 'Delivery cost (PLN)', 'Min order cost (PLN)'])
# df.to_csv('Restaurants_in_Warsaw_via_pyszne.csv', index=False)

# append data to the existing df
df = pd.read_csv('Restaurants_in_Warsaw_via_pyszne.csv')
new_data = pd.DataFrame(zippedList,
                        columns=['Name', 'District', 'Postal code', 'Kitchens',
                                 'Delivery cost (PLN)', 'Min order cost (PLN)'])
df = df.append(new_data).drop_duplicates(subset=['Name',
                                                 'District',
                                                 'Kitchens',
                                                 'Delivery cost (PLN)',
                                                 'Min order cost (PLN)'])
df.to_csv('Restaurants_in_Warsaw_via_pyszne.csv', index=False)

end_time = time.time()
print(end_time - start_time)
