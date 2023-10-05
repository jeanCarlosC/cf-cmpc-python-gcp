from database.entities.validacion_proforma import ValidacionProforma
class postgressRepository():
    def __init__(self, db):
        self.db = db
    def get_validacion_proforma_by_order_id(self, order_id):
        data = self.db.fetch_one(f"SELECT order_id, user_id, fecha_hora, url_archivo, status FROM validacion_proforma WHERE order_id = '{order_id}'")
        if data:
            return ValidacionProforma(order_id=data[0], user_id=data[1], fecha_hora=data[2], url_archivo=data[3], status=data[4])
        return None

    def insert_validacion_proforma(self, validacion_proforma):
        return self.db.execute(f"INSERT INTO validacion_proforma (order_id, user_id, fecha_hora, url_archivo, status) VALUES ('{validacion_proforma.order_id}', '{validacion_proforma.user_id}', '{validacion_proforma.fecha_hora}', '{validacion_proforma.url_archivo}', {validacion_proforma.status})")
    def update_validacion_proforma(self, validacion_proforma):
        return self.db.execute(f"UPDATE validacion_proforma SET user_id ='{validacion_proforma.user_id}', fecha_hora = '{validacion_proforma.fecha_hora}', url_archivo = '{validacion_proforma.url_archivo}', status = {validacion_proforma.status}  WHERE order_id = '{validacion_proforma.order_id}'")