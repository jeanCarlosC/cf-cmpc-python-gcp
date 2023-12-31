# cf-cmpc-python-gcp
Función para generar validaciones de proformas de ordenes de venta

### Descripción

Esta función que es activada mediante un trigger de cloud storage (especificamente cuando se escriben archivos en el bucket) tiene como objetivo registrar una nueva validación de archivo (proforma) que luego el cliente validará en su sistema.

### Construcción 🛠️
* **Tipo:** Cloud Function
* **Lenguaje:** Python 3.9
* **Framework:** Flask
* **Base de datos:** PostgreSQL

### Autor ✒️
* **Autores:** Jean Carlos Cuadros, cuadrosjean26@gmail.com.

### Información sobre estructura del proyecto 📖

El proyecto está organizado de la siguiente manera:

- `src/`: Contiene la lógica de la aplicación.
- `sql-scripts/`: Contiene los scripts de la base de datos.
- `src/database`: Contiene la implementación de la base de datos.
- `src/database/base.py`: Implementación de la clase base para los modelos.
- `src/database/sqlalchemy.py`: Implementación del ORM SQLAlchemy.
- `src/database/sqlalchemy_repository`: Implementación del repositorio para comunicarse con el ORM SQLAlchemy.
- `src/database/entities`: Contiene las entidades de la base de datos.
- `src/database/models`: Contiene los modelos de las entidades de la base de datos.
- `src/main.py`: Inicialización de dependencias para luego iniciar la función.


### Pre-requisitos 📋

- Docker.

### Instalación 🔧

- Clonar proyecto.
- Crear archivo `.env` en la carpeta raíz. Se incluye archivo `.env.example` como referencia, que se puede usar tal cual como está.
- Ejecutar `docker-compose build` para construir las imágenes de Docker. Sólo es necesario hacerlo una vez.
- Ejecutar `docker-compose up` para levantar los servicios. Si se quiere ejecutar en segundo plano, usar `docker-compose up -d`.

### Información de cómo realizar las pruebas de la base de datos 📖

Podemos acceder a la base de datos `proformas` ingresando al contenedor `database_postgres` usando el usuario `admin` con el siguiente comando:

    ```bash
    docker exec -it database_postgres psql -U admin -d proformas
    ```

luego podriamos consultar la tabla `validacion_proforma` ingresando la siguiente query de ejemplo:
    
    ```sql
    SELECT * FROM validacion_proforma;
    ```
o editar un registro de la tabla `validacion_proforma` ingresando la siguiente query de ejemplo:

    ```sql
    UPDATE validacion_proforma SET status = 2 WHERE order_id = '1' AND url_archivo = 'https://storage.cloud.google.com/bucket-name/Ack_1_1_04102023221024.pdf';
    ```

### Información de cómo realizar las pruebas de la función de manera LOCAL 📖
La función está corriendo en el contenedor `cf-validacion-proforma` de forma que maneje y simule eventos generados por servicios de Google Cloud, en este caso cuando se escriba un archivo en el bucket de Cloud Storage.

Para probar la función se hace una petición `POST` a la URL local `http://localhost:2626` con el siguiente body de ejemplo:

- **Url**: `http://localhost:2626`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body** (ejemplo):
```json
{
    "data": {
        "bucket": "bucket-name",
        "name": "Ack_1_1_04102023221024.pdf",
        "size": "211624"
    },
    "eventId": "2523523521",
    "timestamp": "2023-10-04T22:11:01.061Z",
    "eventType": "google.storage.object.finalize",
    "resource": {
        "name": "gs://bucket-name/Ack_1_1_04102023221024.pdf",
        "service": "storage.googleapis.com",
        "type": "storage#object"
    }
}
```

donde el atributo `data` contiene la información del evento generado por Cloud Storage, y el resto es información del contexto del evento.

- `data.bucket`: es el nombre del bucket donde se escribió el archivo.
- `data.name`: es el nombre del archivo
- `data.size`: es el tamaño del archivo en bytes.
- `eventId`: es el id del evento.
- `timestamp`: es la fecha y hora en que se generó el evento.
- `eventType`: es el tipo de evento.
- `resource.name`: es la ruta del archivo en el bucket.
- `resource.service`: es el servicio que generó el evento.
- `resource.type`: es el tipo de recurso.

de los cuales los que se ocupan para la función son `data.bucket`, `data.name`

**NOTA**: El nombre del archivo debe tener el siguiente formato `Ack_order_id_user_id_ddmmyyyyhhmmss.pdf` donde `order_id` es el id de la orden de venta, `user_id` es el id del usuario que generó la orden de venta, y `ddmmyyyyhhmmss` es la fecha y hora en que se generó la orden de venta.


### Información de cómo realizar las pruebas de la función de manera REMOTA en GCP 📖
El proceso de activación de la función es de la siguiente manera:

- Se escribe un archivo en el bucket de cloud storage.
- **Se genera un evento en el bucket de cloud storage**: Cloud Storage está diseñado para monitorear un depósito (bucket) en busca de eventos específicos. en este caso es cuando se escribe un archivo en el bucket.
- **Se notifica al servicio de Cloud Functions**: Cuando se detecta un evento en el depósito de Cloud Storage, el sistema de Google Cloud envía una notificación al servicio de Cloud Functions, que a su vez sabe qué función debe activar (por como desplegamos la función).
- **Ejecución de la función**: La Cloud Function que se configuró para ese desencadenador específico se ejecuta automáticamente y recibe información sobre el evento (nombre del archivo, nombre del bucket , ..).

El archivo cloudbuild.yaml contiene la configuración para realizar el despliegue de la función en GCP, para ello se debe tener en cuenta lo siguiente:

#### Servicios a los que se debe tener acceso en un proyecto de GCP:
- Cloud Repositories
- Cloud Build
- Cloud Storage
- Secret Manager

#### Preparar la nube:
- Crear repositorio en google cloud repositories con el nombre que definas (ejemplo `cf-validacion-proforma`), luego subir este proyecto al mismo. https://source.cloud.google.com/repo/create

- Se debe contar con un bucket en google cloud storage con el nombre que se defina, ese nombre luego lo usaras para configurar el activador de cloud build. https://console.cloud.google.com/storage/browser
- Se debe tener un secret manager con el nombre que se defina (ejemplo `cf-validacion-proforma`) que contenga las variables de entorno que se encuentran en el archivo `.env.example`. https://console.cloud.google.com/security/secret-manager
- Se debe crear un trigger de cloud build con el nombre que se defina (ejemplo `cf-validacion-proforma`) que apunte al repositorio en cloud repositories de la función, que se active mediante la rama que definas (ejemplo `master`) y que ejecute el archivo `cloudbuild.yaml` que se encuentra en la raíz del proyecto. https://console.cloud.google.com/cloud-build/triggers
- Define las sigientes variales de sustitución dentro del trigger de cloud build:
    - `_SECRET`: es el nombre del secret manager que se creó anteriormente.
    - `_PROJECT_ID`: es el id del proyecto de GCP.
    - `_BUCKET`: es el nombre del bucket de cloud storage que se creó anteriormente. (formato ejemplo: `gs://bucket-name`).
- Ejecutar activador y esperar que se despliegue la función, luego podrás verla en el listado de funciones de tu proyecto en GCP. https://console.cloud.google.com/functions/list


Luego que la función este desplegada y andando, sube un archivo PDF al bucket de cloud storage que creaste anteriormente, y verifica que se haya registrado la validación en la base de datos.

tambien podrías revisar los logs de la función en GCP para verificar que todo este bien.