from flask import Flask, request
from loguru import logger

from controllers.car_controller import create_owner, create_car, get_owners, get_owner_cars, update_owner_sale_opportunity, get_owner_info, delete_car_by_id, get_car_info
from models.car_owner import db, create_tables
from utils.returner import return_json
from utils.validator import validate_color, validate_model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    create_tables()
_CAR_LIMIT = 3

##POST
@app.route('/add_owner', methods=['POST'])
def add_owner():
    if not request.json:
        return return_json(204, "No content")

    create_owner(request.json['name'])
    return return_json(200, "Success")

@app.route('/owners', methods=['GET'])
def get_all_owners():
    return return_json(200, "Success", get_owners())

@app.route('/add_car', methods=["POST"])
def add_car():
    if not request.json:
        return return_json(204, "No content")

    if 'owner_id' not in request.json:
        return return_json(401, 'owner_id needed')

    if 'model' not in request.json:
        return return_json(401, 'model needed')

    if not validate_model(request.json['model']):
        return return_json(401, "model not valid")

    if 'color' not in request.json:
        return return_json(401, 'color needed')

    if not validate_color(request.json['color']):
        return return_json(401, "color not valid")

    if not get_owner_info(request.json['owner_id']):
        return return_json(401, 'select a valid owner')

    owner_qtd_car = len(get_owner_cars(request.json['owner_id']))

    if owner_qtd_car >= _CAR_LIMIT:
        return return_json(401, "Owner already has 3 cars")

    create_car(request.json['color'], request.json['model'], request.json['owner_id'])
    owner_qtd_car = len(get_owner_cars(request.json['owner_id']))

    if owner_qtd_car == _CAR_LIMIT:
        update_owner_sale_opportunity(request.json['owner_id'])

    return return_json(200, "Success")

##GET

@app.route('/get_cars', methods=["GET"])
def get_all_cars():
    if 'owner_id' not in request.json:
        return return_json(401, 'owner_id needed')

    cars = get_owner_cars(request.json['owner_id'])
    if cars:
        return return_json(200, "Success", cars)

    return return_json(404, "car not found")

##DELETE

@app.route('/delete_car', methods=['DELETE'])
def delete_car():
    if 'car_id' not in request.json:
        return return_json(401, 'car_id needed')
    car_info = get_car_info(request.json['car_id'])

    if not car_info:
        return return_json(404, "car not found")

    delete_car_by_id(request.json['car_id'])
    update_owner_sale_opportunity(car_info.owner_id,True)

    return return_json(200, "Success")


if __name__ == '__main__':
    app.run(debug=True)


#docker build -t my_flask_app .
#docker run -p 5000:5000  my_flask_app
# docker run --rm my_flask_app pytest