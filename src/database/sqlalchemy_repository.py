from database.models import ValidacionProforma as ValidacionProformaModel


class postgressRepository():
    def __init__(self, SqlAlchemyClient):
        self.session_factory = SqlAlchemyClient.session_factory
        self.validacion_proforma_model = ValidacionProformaModel

    def get_validacion_proforma_by_order_id(self, order_id):
        with self.session_factory() as session:
            validacion_proforma = session.query(self.validacion_proforma_model)\
                .filter_by(order_id=order_id)\
                .order_by(self.validacion_proforma_model.fecha_hora.desc())\
                .first()
            if validacion_proforma:
                return self._format_to_entity(validacion_proforma)
            return None

    def insert_validacion_proforma(self, validacion_proforma):
        new_validacion_proforma = self.validacion_proforma_model(
            order_id=validacion_proforma.get("order_id"),
            user_id=validacion_proforma.get("user_id"),
            fecha_hora=validacion_proforma.get("fecha_hora"),
            url_archivo=validacion_proforma.get("url_archivo"),
            status=validacion_proforma.get("status")
        )
        with self.session_factory() as session:
            session.add(new_validacion_proforma)
            session.commit()
            return self._format_to_entity(new_validacion_proforma)

    def update_validacion_proforma(self, order_id, url_archivo, validacion_proforma):
        with self.session_factory() as session:
            session.query(self.validacion_proforma_model)\
                .filter_by(order_id=order_id)\
                .filter_by(url_archivo=url_archivo)\
                .update(validacion_proforma)
            session.commit()
            return True

    def _format_to_entity(self, model):
        return model.to_entity()
