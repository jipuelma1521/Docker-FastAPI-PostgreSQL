# Proyecto 21 — Docker + FastAPI + PostgreSQL

Proyecto práctico para aprender los fundamentos de Docker y Docker Compose utilizando una API en FastAPI conectada a una base de datos PostgreSQL.

## Objetivos

En este proyecto aprendí a trabajar con:

- Docker Desktop
- Imágenes y contenedores
- Dockerfile
- Puertos
- Bind mounts
- Volúmenes persistentes
- PostgreSQL dentro de Docker
- Docker Compose
- Redes internas entre contenedores
- Variables de entorno
- `.env`
- `.gitignore`
- `.dockerignore`
- Logs y comandos básicos de Docker

## Arquitectura

La aplicación está formada por dos servicios:

```text
Navegador
    |
    | localhost:8000
    v
FastAPI
    |
    | db:5432
    v
PostgreSQL
    |
    v
Volumen persistente
postgres-data
```

FastAPI y PostgreSQL se ejecutan en contenedores separados.

Docker Compose crea una red interna que permite que FastAPI se conecte al servicio PostgreSQL utilizando el hostname:

```text
db
```

## Estructura

```text
docker-primer-proyecto/
├── app.py
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .env
├── .gitignore
├── .dockerignore
└── README.md
```

El archivo `.env` contiene variables de entorno y no se sube al repositorio.

## Dockerfile

La imagen de FastAPI se construye usando Python 3.13 Slim.

El Dockerfile:

1. Parte desde una imagen Python.
2. Crea `/app` como directorio de trabajo.
3. Instala las dependencias.
4. Copia la aplicación.
5. Ejecuta Uvicorn.

## Docker Compose

Docker Compose administra dos servicios:

### API

- FastAPI
- Puerto `8000`
- Construida desde el Dockerfile

### Base de datos

- PostgreSQL
- Puerto `5432`
- Base de datos `scientific_db`
- Datos almacenados en un volumen persistente

## Volumen persistente

PostgreSQL utiliza:

```text
postgres-data
```

Esto permite que los datos sobrevivan incluso si el contenedor PostgreSQL es eliminado y creado nuevamente.

## Variables de entorno

La configuración se carga desde `.env`.

Ejemplo:

```text
POSTGRES_PASSWORD=...
POSTGRES_DB=scientific_db
POSTGRES_USER=postgres
DB_HOST=db
```

Las credenciales reales no se almacenan en GitHub.

## Ejecutar el proyecto

Construir y levantar los servicios:

```bash
docker compose up -d --build
```

Ver los contenedores:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs api
docker compose logs db
```

Detener los servicios:

```bash
docker compose down
```

## API

Página principal:

```text
http://localhost:8000
```

Experimentos:

```text
http://localhost:8000/experimentos
```

Documentación automática de FastAPI:

```text
http://localhost:8000/docs
```

## Comandos Docker aprendidos

```bash
docker ps
docker ps -a
docker images
docker volume ls

docker build -t nombre-imagen .

docker run nombre-imagen

docker stop nombre-contenedor
docker start nombre-contenedor
docker rm nombre-contenedor

docker logs nombre-contenedor

docker exec -it nombre-contenedor bash

docker compose up -d
docker compose up -d --build
docker compose down
docker compose ps
docker compose logs
```

## Conceptos principales

### Imagen

Plantilla inmutable utilizada para crear contenedores.

### Contenedor

Instancia ejecutándose a partir de una imagen.

### Dockerfile

Archivo que describe cómo construir una imagen.

### Volumen

Almacenamiento persistente independiente del ciclo de vida de un contenedor.

### Puerto

Permite conectar un servicio dentro de un contenedor con el sistema host.

Ejemplo:

```text
8000:8000
```

### Docker Compose

Permite definir y ejecutar varios servicios relacionados desde un único archivo.

## Resultado

El proyecto implementa una aplicación FastAPI y una base de datos PostgreSQL completamente contenerizadas.

Los servicios pueden levantarse conjuntamente mediante:

```bash
docker compose up -d --build
```

FastAPI se comunica con PostgreSQL utilizando la red interna creada automáticamente por Docker Compose.

Los datos de PostgreSQL se mantienen de forma persistente mediante un volumen Docker.