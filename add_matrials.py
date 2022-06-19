import csv
from main import Matrial, Category, Delivery
def add_material(matrials):
    for material in matrials:
        m = Matrial(name=material)
        m.add()

def add_category(matrials):
    for material in matrials:
        m = Category(name=material)
        m.add()

def add_delivery():
    ## first deleivey 
    delivery = Delivery(name='Zaki', address="giza", phone = '0127222222')
    delivery.add()
    ## second deleivey 
    delivery = Delivery(name='Hossam', address="haram", phone = '0111056464')
    delivery.add()
    
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
        line_count += 1
    print(f'Processed {line_count} lines.')
    
# add_delivery()