from main import Customer, Category , Matrial , Delivery, SellCategorymatrial , PublicIdAuto

## autoicreament 
# public_id  = PublicIdAuto(id=91)
# public_id.add()

# customer = Customer(first_name='mohamed', last_name='ali', email='mdiaa442@gmail.com', password='12345678', address='october', phone='01274666163', points=0.0, public_id=public_id.id)
# customer.add()



'''
glass, paper, cardboard, tires, textiles, batteries, and electronics.
'''

# matrial = Matrial(name='electronics')
# matrial.add()

# category  = Category(name='chair')
# category.add()


 
# delivery = Delivery(name='ahmed', address="giza", phone = '01222222')
# delivery.add()




# customer make new order 
# sell_category_matrial = SellCategorymatrial(matrial_id=2, category_id=1 , delivery_id=1, customer_id=5, date="2022-05-20", time='5:30', weight=5, points=30, done=False)
# sell_category_matrial.add()
# print(SellCategorymatrial.query.all()[0].done)