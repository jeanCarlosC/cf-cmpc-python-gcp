from flask import jsonify
from google.cloud import storage
from datetime import datetime
from database.postgress import postgress
from database.entities.validacion_proforma import ValidacionProforma
from database.postgress_repository import postgressRepository


def validacionProforma(event, context):
    db = postgress()
    postgress_repository = postgressRepository(db)
    file_name = event["name"]
    order_id, user_id, date_time = split_file_name(file_name)
    validacion_proforma = ValidacionProforma(
        order_id, user_id, date_time, file_name, 0)
    validacion_exist = postgress_repository.get_validacion_proforma_by_order_id(
        order_id)
    if validacion_exist:
        if validacion_exist.status == 1:
            raise Exception(
                "La proforma ya fue validada por el cliente")
        postgress_repository.update_validacion_proforma(validacion_proforma)
    else:
        postgress_repository.insert_validacion_proforma(validacion_proforma)
    db.close()
    return "OK", 200


def split_file_name(file_name):
    print("file_name", file_name)
    file_name_split = file_name.split("_")
    order_id = file_name_split[1]
    user_id = file_name_split[2]
    date_time = file_name_split[3].split(".")[0]
    date_time = format_date_time(date_time)
    return order_id, user_id, date_time


def format_date_time(date_time):
    # date_time tiene este formato ddmmyyyyhhmmss se debe convertir a yyyy-mm-dd hh:mm:ss
    date_time = datetime.strptime(
        date_time, '%d%m%Y%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    return date_time
