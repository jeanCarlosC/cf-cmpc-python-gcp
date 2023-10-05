from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ValidacionProforma:

    order_id: str
    user_id: str
    fecha_hora: datetime
    url_archivo: str
    status: int

    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return ValidacionProforma(
            order_id=data.get('order_id'),
            user_id=data.get('user_id'),
            fecha_hora=data.get('fecha_hora'),
            url_archivo=data.get('url_archivo'),
            status=data.get('status')
        )