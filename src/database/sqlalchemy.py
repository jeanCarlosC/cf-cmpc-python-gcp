import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry
from sqlalchemy.engine import url

"""
Conexión a una base de datos SQL por medio del ORM SQL Alchemy.
"""

class SQLAlchemyClient():

    def __init__(self):

        # Obtener datos desde variables de entorno.

        driver = os.environ["SQL_ALCHEMY_DRIVER"]
        username = os.environ["SQL_ALCHEMY_USERNAME"]
        password = os.environ["SQL_ALCHEMY_PASSWORD"]
        database = os.environ["SQL_ALCHEMY_DATABASE"]

        # Obtener el host o el socket. Sólo se usa uno de los dos para la conexión.
        # El socket es útil para conectarse con una base de datos en GCP.
        
        host = os.environ.get("SQL_ALCHEMY_HOST", None)
        socket = os.environ.get("SQL_ALCHEMY_SOCKET", None)
        
        socket_query = None

        if host:
            socket = None

        elif socket:
            socket_query = {
                "unix_socket": "/cloudsql/%s" % socket
            }
        db_url = url.URL.create(
            drivername = driver,
            username = username,
            password = password,
            database = database,
            host = host,
            query = socket_query,
        )
        
        self.engine = create_engine(db_url, echo=False)
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False, autoflush=True)
        self.mapper_registry = registry()