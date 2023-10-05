from database.entities.validacion_proforma import ValidacionProforma as ValidacionProformaEntity
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON
from database.base import Base

class ValidacionProforma(Base):
    __tablename__ = 'validacion_proforma'
    order_id = Column(String, primary_key=True)
    user_id = Column(String)
    fecha_hora = Column(TIMESTAMP)
    url_archivo = Column(String)
    status = Column(Integer)

    def __init__(self, order_id, user_id, fecha_hora, url_archivo, status):
        self.order_id = order_id
        self.user_id = user_id
        self.fecha_hora = fecha_hora
        self.url_archivo = url_archivo
        self.status = status
    
    def to_entity(self):
        return ValidacionProformaEntity(
            order_id=self.order_id,
            user_id=self.user_id,
            fecha_hora=self.fecha_hora,
            url_archivo=self.url_archivo,
            status=self.status
        )