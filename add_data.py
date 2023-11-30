import csv
from main import app, Matrial, Category, Delivery, Zone

def add_material(matrials):
    for material in matrials:
        m = Matrial(name=material)
        m.add()

def add_category(matrials):
    for material in matrials:
        m = Category(name=material)
        m.add()

def add_zones(zones):
    for zone in zones:
        z = Zone(name=zone)
        z.add()

def add_delivery():
    ## first deleivey 
    delivery = Delivery(name='Zaki',  phone = '0127222222', email='zaki@bikya.com', password="zaki123", zone_id=1)
    delivery.add()
    ## second deleivey 
    delivery = Delivery(name='Hossam',  phone = '0127222222', email='hosam@bikya.com', password="hosam123", zone_id=2)
    delivery.add()
    ## third deleivey 
    delivery = Delivery(name='Mohaned',  phone = '0127222222', email='mohaned@bikya.com', password="mohaned123", zone_id=3)
    delivery.add()


with app.app_context() :
    with open('data/material.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            print(row)
            # matrial 
            if line_count == 0:
                add_material(row)                        
            elif line_count == 1:
                add_category(row)                    
            elif line_count == 2:
                add_zones(row)
            line_count += 1
        print(f'Processed {line_count} lines.')

    add_delivery()
