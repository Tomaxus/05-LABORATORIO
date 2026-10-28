# API REST de biblioteca

API desarrollada con Django para administrar libros y editoriales almacenados en MongoDB Atlas. Todas las respuestas se entregan en JSON y los endpoints pueden probarse con Postman, Thunder Client o cURL.

## Tecnologías

- Python 3.13
- Django 6.1
- MongoDB Atlas
- `django-mongodb-backend`

## Instalación

1. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

2. Crea un archivo `.env` en la raíz del proyecto:

   ```env
   MONGODB_URI=mongodb+srv://usuario:contraseña@cluster.mongodb.net/
   MONGODB_NAME=devconf
   ```

3. Inicia el servidor:

   ```bash
   python manage.py runserver
   ```

La API estará disponible en `http://127.0.0.1:8000/api/`.

## Estructura

```text
devconf/
  settings.py       configuración de Django y MongoDB
  urls.py           rutas principales
devconfsite/
  models.py         modelos Libro y Editorial
  views.py          endpoints REST y respuestas JSON
  urls.py           rutas de la API
manage.py           comando de administración de Django
requirements.txt    dependencias del proyecto
```

## Endpoints

### Libros

| Método | Ruta | Resultado |
|---|---|---|
| GET | `/api/libros/` | Lista todos los libros |
| POST | `/api/libros/` | Crea un libro |
| GET | `/api/libros/<id>/` | Consulta un libro |
| PUT | `/api/libros/<id>/` | Reemplaza los datos de un libro |
| PATCH | `/api/libros/<id>/` | Actualiza parcialmente un libro |
| DELETE | `/api/libros/<id>/` | Elimina un libro |

Para crear o actualizar un libro, envía este JSON:

```json
{
  "titulo": "El alquimista",
  "anio": 1988,
  "paginas": 192,
  "imagen": "el-alquimista.jpg",
  "editorial_id": "ID_DE_LA_EDITORIAL"
}
```

### Editoriales

| Método | Ruta | Resultado |
|---|---|---|
| GET | `/api/editoriales/` | Lista todas las editoriales |
| POST | `/api/editoriales/` | Crea una editorial |
| GET | `/api/editoriales/<id>/` | Consulta una editorial y sus libros |
| PUT | `/api/editoriales/<id>/` | Reemplaza los datos de una editorial |
| PATCH | `/api/editoriales/<id>/` | Actualiza parcialmente una editorial |
| DELETE | `/api/editoriales/<id>/` | Elimina una editorial |

Para crear o actualizar una editorial, envía:

```json
{
  "nombre": "Planeta",
  "pais": "España"
}
```

## Códigos HTTP

- `200 OK`: consulta o actualización exitosa.
- `201 Created`: recurso creado.
- `204 No Content`: recurso eliminado.
- `400 Bad Request`: JSON inválido o datos incompletos.
- `404 Not Found`: recurso inexistente.
- `405 Method Not Allowed`: método HTTP no permitido para la ruta.

## Ejemplo con cURL

```bash
curl http://127.0.0.1:8000/api/libros/
```

```bash
curl -X POST http://127.0.0.1:8000/api/editoriales/ ^
  -H "Content-Type: application/json" ^
  -d "{\"nombre\":\"Planeta\",\"pais\":\"España\"}"
```

## Pruebas desde la terminal

El archivo [probar-api.ps1](probar-api.ps1) ejecuta las mismas operaciones desde PowerShell y muestra cada método, URL, código HTTP y respuesta en la terminal.

Con el servidor Django ejecutándose, abre otra terminal en la raíz del proyecto y ejecuta:

```powershell
.\probar-api.ps1
```

Para usar otra dirección de API:

```powershell
.\probar-api.ps1 -BaseUrl "http://localhost:8000/api"
```

Si PowerShell bloquea la ejecución de scripts, permite scripts para la sesión actual:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\probar-api.ps1
```

## Autor

Tomás Uribe Sánchez  
Estudiante de Ingeniería de Sistemas e Informática  
Universidad Pontificia Bolivariana
