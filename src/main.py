from datetime import datetime
from database.sqlalchemy import SQLAlchemyClient
from database.sqlalchemy_repository import postgressRepository
SqlAlchemyClient = SQLAlchemyClient()


def validacionProforma(event, context):
    postgress_repository = postgressRepository(SqlAlchemyClient)
    file_name = event["name"]
    bucket_name = event["bucket"]
    url_archivo = f"https://storage.cloud.google.com/{bucket_name}/{file_name}"
    order_id, user_id, date_time = split_file_name(file_name)
    dict_validacion_proforma = {
        "order_id": order_id,
        "user_id": user_id,
        "fecha_hora": date_time,
        "url_archivo": url_archivo,
        "status": 0
    }
    print("bucket {} file {}".format(bucket_name, file_name))
    validacion_exist = postgress_repository.get_validacion_proforma_by_order_id(
        order_id)
    if validacion_exist and validacion_exist.status == 1:
        raise Exception(
            "La proforma ya fue validada por el cliente")
    elif validacion_exist and validacion_exist.status == 0:
        print("Se edita la validacion")
        postgress_repository.update_validacion_proforma(order_id,validacion_exist.url_archivo,
            dict_validacion_proforma)
    else:
        print("Se crea una nueva validacion")
        postgress_repository.insert_validacion_proforma(
            dict_validacion_proforma)
    return "OK", 200


def split_file_name(file_name):
    file_name_split = file_name.split("_")
    if len(file_name_split) != 4 or file_name_split[0] != "Ack" or file_name_split[3].split(".")[1] != "pdf":
        raise Exception(
            "El nombre del archivo no cumple con el formato requerido")
    order_id = file_name_split[1]
    user_id = file_name_split[2]
    date_time_split = file_name_split[3].split(".")
    date_time = format_date_time(date_time_split[0])
    return order_id, user_id, date_time


def format_date_time(date_time):
    # validar que el string tenga solo numeros
    if not date_time.isdigit() or len(date_time) != 14:
        raise Exception(
            "El formato de fecha y hora en el nombre del archivo no es correcto")
    try:
        date_time = datetime.strptime(
            date_time, '%d%m%Y%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        return date_time
    except ValueError:
        raise Exception(
            "El formato de fecha y hora en el nombre del archivo no es correcto")
