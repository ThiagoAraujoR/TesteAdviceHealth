from flask import jsonify

def return_json(status_code:int, message:str, data:dict={}):
    return jsonify({
        "status_code": status_code,
        "message": message,
        "data": data,
    })