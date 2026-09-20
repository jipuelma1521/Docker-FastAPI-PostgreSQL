
# Proyectos 21 y 22 — Docker + FastAPI + PostgreSQL + CI/CD

Proyecto práctico para aprender los fundamentos de Docker, Docker Compose y CI/CD utilizando una API en FastAPI conectada a una base de datos PostgreSQL.

El Proyecto 21 implementa la aplicación contenerizada.

El Proyecto 22 incorpora pruebas automatizadas, GitHub Actions y publicación de imágenes Docker en GitHub Container Registry.

## Objetivos

### Proyecto 21 — Docker

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

### Proyecto 22 — CI/CD

En este proyecto aprendí a trabajar con:

- Testing automatizado con pytest
- TestClient de FastAPI
- Entornos virtuales de Python
- GitHub Actions
- Workflows y archivos YAML
- Jobs y steps
- Runners de GitHub
- Continuous Integration (CI)
- Construcción automática de imágenes Docker
- Dependencias entre jobs
- GitHub Container Registry (GHCR)
- Publicación automática de imágenes Docker
- Continuous Delivery (CD)
- GITHUB_TOKEN y permisos de GitHub Actions

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
|
|-- app.py
|-- Dockerfile
|-- compose.yaml
|-- requirements.txt
|-- .env
|-- .gitignore
|-- .dockerignore
|-- README.md
|
|-- tests/
|   |-- test_main.py
|
|-- .github/
    |-- workflows/
        |-- ci.yml
```

El archivo `.env` contiene variables de entorno y no se sube al repositorio.

El entorno virtual `.venv` tampoco debe subirse a GitHub.

## Dockerfile

La imagen de FastAPI se construye usando Python 3.13 Slim.

El Dockerfile:

1. Parte desde una imagen Python.
2. Crea `/app` como directorio de trabajo.
3. Instala las dependencias.
4. Copia la aplicación.
5. Ejecuta Uvicorn.

## Docker Compose

Docker Compose administra dos servicios.

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

http://localhost:8000

Experimentos:

http://localhost:8000/experimentos

Documentación automática de FastAPI:

http://localhost:8000/docs

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

## Conceptos principales de Docker

### Imagen

Plantilla utilizada para crear contenedores.

### Contenedor

Instancia creada a partir de una imagen, que puede ejecutarse como un proceso aislado.

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

---

# Proyecto 22 — CI/CD

## ¿Qué es CI/CD?

CI/CD es un conjunto de prácticas que permite automatizar las pruebas, construcción y entrega de aplicaciones.

### Continuous Integration (CI)

Cada vez que se sube código a GitHub, un sistema automatizado comprueba que el proyecto siga funcionando.

En este proyecto, CI ejecuta pruebas con pytest y construye una imagen Docker.

### Continuous Delivery (CD)

Permite dejar automáticamente una nueva versión de la aplicación preparada para su despliegue.

En este proyecto, publicamos la imagen Docker en GitHub Container Registry.

Todavía no desplegamos automáticamente la aplicación en un servidor.

## Testing con pytest

Se incorporó pytest para comprobar automáticamente el funcionamiento de la API.

El archivo:

```text
tests/test_main.py
```

contiene una prueba del endpoint principal de FastAPI.

```python
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "mensaje": "FastAPI funcionando dentro de Docker Compose"
    }
```

El test comprueba que:

1. La API responde a una petición HTTP GET.
2. El código HTTP es 200.
3. El JSON contiene el mensaje esperado.

Para ejecutar los tests:

```bash
python -m pytest
```

Si todo funciona:

```text
1 passed
```

Si la respuesta no coincide con lo esperado, pytest informa del fallo.

El endpoint `/experimentos` requiere PostgreSQL y no está cubierto por este test inicial.

## GitHub Actions

GitHub Actions permite ejecutar tareas automáticamente cuando ocurren determinados eventos en el repositorio.

En este proyecto configuramos un workflow que se activa cuando hacemos:

```bash
git push
```

También se ejecuta ante eventos de pull request.

El workflow está definido en:

```text
.github/workflows/ci.yml
```

## Pipeline CI/CD

El pipeline implementado tiene la siguiente estructura:

```text
Desarrollador
     |
     v
git push
     |
     v
GitHub Actions
     |
     v
Job 1: test
     |
     | Instalar Python
     | Instalar dependencias
     | Ejecutar pytest
     |
     v
Tests exitosos
     |
     v
Job 2: docker
     |
     | Construir imagen Docker
     | Iniciar sesion en GHCR
     | Publicar imagen Docker
     |
     v
GitHub Container Registry
```

El segundo job utiliza:

```yaml
needs: test
```

Esto significa que solamente se ejecuta cuando el primer job termina correctamente.

## Archivo ci.yml

El workflow utiliza:

- `push`: activa la automatización al subir código.
- `pull_request`: activa la automatización en pull requests.
- `runs-on`: especifica la máquina utilizada.
- `steps`: define las operaciones que ejecuta cada job.
- `uses`: utiliza acciones existentes.
- `run`: ejecuta comandos.
- `needs`: establece dependencias entre jobs.
- `permissions`: define los permisos del token de GitHub.

El pipeline utiliza máquinas Ubuntu proporcionadas temporalmente por GitHub Actions.

## Experimento: romper el código intencionalmente

Para comprobar el funcionamiento del sistema, modificamos temporalmente la respuesta del endpoint principal:

```python
return {"mensaje": "FastAPI roto"}
```

El test esperaba:

```python
{"mensaje": "FastAPI funcionando dentro de Docker Compose"}
```

Al ejecutar pytest, obtuvimos:

```text
1 failed
```

Después subimos el cambio a GitHub.

GitHub Actions detectó automáticamente el error y marcó el workflow como fallido.

Finalmente restauramos el código original y ejecutamos nuevamente el pipeline.

Resultado:

```text
CI #1: SUCCESS
CI #2: FAILURE
CI #3: SUCCESS
```

Este experimento permitió comprobar que CI detecta cambios que rompen comportamientos cubiertos por las pruebas.

## Integración con Docker

Se agregó un segundo job encargado de construir automáticamente la imagen Docker.

Comando utilizado:

```bash
docker build -t ghcr.io/jipuelma1521/scientific-api:latest .
```

De esta manera, GitHub comprueba que la aplicación puede empaquetarse correctamente.

## GitHub Container Registry

GitHub Container Registry (GHCR) permite almacenar imágenes Docker asociadas a una cuenta de GitHub.

En este proyecto publicamos la imagen:

```text
ghcr.io/jipuelma1521/scientific-api:latest
```

El pipeline inicia sesión utilizando el token temporal proporcionado por GitHub Actions.

Posteriormente ejecuta:

```bash
docker push ghcr.io/jipuelma1521/scientific-api:latest
```

La publicación se realiza automáticamente cuando hacemos push a la rama principal y los tests terminan correctamente.

Los pull requests ejecutan las comprobaciones, pero no publican la imagen.

## ¿Qué conseguimos con CI/CD?

Antes del Proyecto 22, para comprobar y empaquetar una nueva versión teníamos que ejecutar manualmente:

```bash
python -m pytest

docker build -t scientific-api .
```

Ahora GitHub Actions realiza esas operaciones automáticamente.

Además, publica la imagen Docker en un registro desde donde puede descargarse posteriormente.

## Resultado final

El Proyecto 21 implementó una aplicación FastAPI conectada a PostgreSQL mediante Docker Compose.

El Proyecto 22 incorporó un pipeline CI/CD capaz de:

1. Detectar cambios en GitHub.
2. Instalar automáticamente las dependencias.
3. Ejecutar pruebas de FastAPI.
4. Detectar errores en el código probado.
5. Construir una imagen Docker.
6. Publicar la imagen en GitHub Container Registry.

La aplicación todavía no se encuentra desplegada en un servidor público.

La siguiente etapa consiste en estudiar AWS y los fundamentos de Cloud Computing para comprender cómo ejecutar aplicaciones en infraestructura remota.