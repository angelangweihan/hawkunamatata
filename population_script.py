import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hawkunamatata.settings')

import django
django.setup()
from hawkuna.models import Category, Subcategory, CurrentProduct, SoldProduct, UserProfile, Review

def populate():

    North = [
        {'name': 'Chong Pang Market & Food Centre'},
        {'name': 'Marsailing Mall Hawker Centre'},
        {'name': 'Woodlands Street 12 Hawker Centre'},
        {'name': 'Yishun Park Hawker Centre'}]

    East = [
        {'name': 'Bedok 85 (Fengshan Food Centre)'},
        {'name': 'Bedok Interchange Food Centre'},
        {'name': 'Marine Parade Food Centre'},
        {'name': 'Old Airport Road Food Centre'}]
        
    Northeast = [
        {'name': 'Broadway Food Centre'},
        {'name': 'Ci Yuan Hawker Centre'},
        {'name': 'Kovan 209 Market & Food Centre'},
        {'name': 'Serangoon Garden Food Centre'}]
        
    South = [
        {'name': 'ABC Brickworks Food Centre'},
        {'name': 'Alexandra Village Food Centre'},
        {'name': 'Redhill Food Centre'},
        {'name': 'Zion Riverside Food Centre'}]

    West = [
        {'name': 'Clementi 448 Food Centre'},
        {'name': 'Commonwealth Crescent Food Centre'},
        {'name': 'Ghim Moh Food Centre'},
        {'name': 'Yuhua Village Market and Food Centre'}]

    Central = [
        {'name': 'Amoy Street Food Centre'},
        {'name': 'Bukit Timah Food Centre'},
        {'name': 'Maxwell Food Centre'},
        {'name': 'Tanjong Pagar Food Centre'}]


        
    categories = {'North': {'subcategories': North},
       'Northeast': {'subcategories': Northeast},
       'East': {'subcategories': East},
       'South': {'subcategories': South},
       'West': {'subcategories': West},
       'Central': {'subcategories': Central},
    }
       




       
    for cat, cat_data in categories.items():
        c = add_cat(cat)
        for p in cat_data['subcategories']:
            add_subcat(c, p['name'])
            
    for c in Category.objects.all():
        for p in Subcategory.objects.filter(category=c):
            print(f'- {c}: {p}')
            
def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c
    
def add_subcat(cat, name):
    s = Subcategory.objects.get_or_create(category=cat, name=name)[0]
    s.save()
    return s

if __name__ == '__main__':
    print('Starting hawkuna-matata population script...')
    populate()
    
