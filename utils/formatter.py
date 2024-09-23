
def format_owners(owners:list):
    dict_owners = {}
    aux = 0
    for owner in owners:
        dict_owners[aux]= {"id":owner.id, "name": owner.name, "is_sale_opportunity": owner.is_sale_opportunity }
        aux+=1
    return dict_owners

def format_cars(cars:list):
    dict_cars = {}
    aux = 0
    for car, owner_name in cars:
        dict_cars[aux]= {"id":car.id, "model": car.model, "color": car.color, "owner": owner_name}
        aux+=1
    return dict_cars