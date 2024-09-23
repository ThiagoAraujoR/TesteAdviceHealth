from models.car_owner import Owner, Car, db
from utils.formatter import format_owners, format_cars
from loguru import logger

##Insert
def create_owner(name:str, is_sale_opportunity:bool=True):
    try:

        owner = Owner(name=name, is_sale_opportunity=is_sale_opportunity)
        db.session.add(owner)
        db.session.commit()
        return owner
    except Exception as e:
        logger.error(e)
def create_car(color, model, owner_id):
    try:
        car = Car(color=color, model=model, owner_id=owner_id)
        db.session.add(car)
        db.session.commit()
        return car
    except Exception as e:
        logger.error(e)

##Select
def get_owners():
    return format_owners(Owner.query.all())

def get_owner_cars(owner_id=0):
    return format_cars(db.session.query(Car, Owner.name).join(Owner).filter(Car.owner_id == owner_id).all())

def get_owner_info(id):
    return Owner.query.filter(id == id).first()

def get_car_info(id):
    return Car.query.filter(id == id).first()

##Update
def update_owner_sale_opportunity(id, is_sale_opportunity=False):
    owner = Owner.query.get(id)

    if owner:
        owner.is_sale_opportunity = is_sale_opportunity
        db.session.commit()
        return owner
    return None

def delete_car_by_id(car_id):
    result = Car.query.filter(Car.id == car_id).delete()
    db.session.commit()
    return result