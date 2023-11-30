
from main import app,  MatrialCategory, Category, Matrial, db

'''
 materials 
  1 | Plastic
  2 | Paper
  3 | Metal
  4 | Glass
  5 | Steel
  6 | Aluminium
  7 | Wood

'''

matrials = [ {'id':1 , 'km_price':20, 'km_points':5},
            {'id':2 , 'km_price':10, 'km_points':3},
            {'id':3 , 'km_price':30, 'km_points':10},
            {'id':4 , 'km_price':15, 'km_points':4},
            {'id':5 , 'km_price':30, 'km_points':10},
            {'id':6 , 'km_price':40, 'km_points':13},
            {'id':7 , 'km_price':20, 'km_points':8},            
            ]

categories = [1, 2, 3, 4, 5, 6]

with app.app_context():
  for matrial in matrials:  
      for i in range(1, 7):
          category_matrial = MatrialCategory(matrial_id=matrial['id'], category_id=i, total_weight=100, km_price=matrial['km_price'] , km_points=matrial['km_points'])
          category_matrial.add()
    

