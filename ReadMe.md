# Instalacion

- Crear based de datos con las tablas, indices e inserciones de datos encontradas en el folder `db`

- Cambiar variable de entorno `DATABASE_URL` en el archivo `.env` por la url de la base de datos creada en el paso anterior. Ejemplo: `DATABASE_URL="postgresql://postgres:admin@host.docker.internal:5432/inventory_management"`

- Correr el comando de docker compose up -d mientras que se esta en el path donde esta la carpeta de la aplicacion.

- Abrir el navegador y acceder a la url http://localhost:8000/docs

# Postman

- Importar el archivo `Postman.json` en postman para realizar las pruebas

# Correr tests

## Unit tests

- Correr el comando `pytest` en la terminal
- Se ocupa cambiar la variable de entorno `DATABASE_URL` en el archivo `.env` por la url con localhost en vez de host.docker.internal. Ejemplo: `DATABASE_URL="postgresql://postgres:admin@localhost:5432/inventory_management"`

## Concurrency tests

- Correr el comando de docker compose up -d mientras que se esta en el path donde esta la carpeta de la aplicacion.

- Correr command de locust -f tests/load/locustfile.py -H http://localhost:8000 en la console. Ingresar a localhost:8089 y ejecutar la cantidad de peticiones que se requieran.

# Despliegue de AWS

## Nota

    No se llego a hacer el despliegue en AWS debido a falta de tiempo y porque la cuenta toma 24 horas en activarse en AWS si se quiere tener este mismo se puede hacer de la siguiente manera:

- Crear RDS en AWS con la siguiente configuracion:

  - Engine: Postgresql
  - Usuario: postgres
  - Password: admin
  - Database name: inventory_management
  - VPC: VPC por defecto
  - Subnet: Subnet por defecto
  - Security group: Security group por defecto
  - Backups: Configuracion predeterminada

- ECR

  - Crear repositorio
  - Subir imagen de docker al ECR

- App Runner

  - Subir imagen en ECR a App Runner
  - Poner variables de entorno en App Runner
  - Usar el endpoint de App Runner para realizar las pruebas

- Api Gateway
  - Crear API Gateway
  - Crear endpoint de API Gateway con integracion de App Runner
  - Usar el endpoint de API Gateway para realizar las pruebas
  - Se puede crear autenticacion por medio de Token

# Diagramas

## AWS Diagram

![Alt text](Diagrams\AWSDiagram.png)

## UML Diagram

![Alt text](Diagrams\UMLDB.png)

# Decisiones tecnicas

Dentro de las pruebas se decidio no hacer un mock de la base de datos debido a el poco tiempo que se tenia para realizar el proyecto. Sin embargo lo correcto seria hacer un mock de esta misma para realizar las pruebas considerando que en esta nueva iteracion se tendria que separar la logica de negocio de la iteraccion con la base de datos. Si se hace esto se podra realizar las pruebas de logica de negocio sin depender de la base de datos y sin ensuciar esta misma.

Se decidio usar FastAPI para el desarrollo de la API, debido a que es un framework moderno y facil de usar, ademas que el desarrollo en este mismo es rapido y proporciona un resultado que es robusto, mantenible y escalable.

Se decidio hacer uso de un contenedor para que este mismo sea facil de mantener, de hacer deploy y que sea facil de escalar.

Por otro lado se decidió usar PostgreSQL para la base de datos, debido a que es una base de datos relacional con gran cantidad de herramientas que pueden llegar a facilitar el desarrollo en un futuro.

Se decidio estructurar el codigo del proyecto por funciones. Una de estas categorias es productos y la otra inventarios. Asi es posible dividir las funcionalidades y dar un mantenimiento mas sencillo.
