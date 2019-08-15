import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Restaurants_in_Warsaw_via_pyszne.csv', delimiter=',')
df['District'].replace({'Polnoc': 'Praga Polnoc', 'Poludnie': 'Praga Poludnie'}, inplace=True)
df['Name'] = df['Name'].str.capitalize()

# Name,District,Postal code,Kitchens,
# Delivery cost (PLN),Min order cost (PLN)
df.drop_duplicates(subset=['Name', 'Delivery cost (PLN)', 'Min order cost (PLN)'], inplace=True)
df = df.groupby(['Name', 'Kitchens']).mean().round(2)
df.to_csv('Restaurants_in_Warsaw_via_pyszne.csv')


def dist_min_order():
    sns.distplot(df['Min order cost (PLN)'], bins=15)
    plt.show()


def dist_del_cost():
    sns.distplot(df['Delivery cost (PLN)'], bins=10)
    plt.show()


def kitchens_unique():
    string = ', '.join(df['Kitchens'].unique())
    listed_unique = list(set(string.split(', ')))
    return listed_unique
