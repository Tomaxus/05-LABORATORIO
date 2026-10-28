# Informe de seguridad — Librería (Django + Next.js)

**Estudiante:** Tomás Uribe Sánchez
**Proyecto:** `Backend/` (API Django REST + MongoDB Atlas, Lab 03) y `Frontend/` (Next.js, Lab 04)
**Rama de trabajo:** `seguridad`

## Parte 0 — Diagnóstico inicial

| Pregunta | Qué se buscó | Sí / No / No aplica |
|---|---|---|
| ⚠ ¿Hay contraseñas guardadas tal cual? | Campos `password`/`clave` | **No aplica** — el proyecto no tiene usuarios |
| ⚠ ¿Hay credenciales en el código? | `SECRET_KEY`, `mongodb+srv` | **Sí** — `SECRET_KEY` escrita en `settings.py` (la URI de Atlas sí está en `.env`) |
| ⚠ ¿Hay archivos de secretos en git? | `git ls-files` | **No** — `.env` está en `.gitignore` |
| ⚠ ¿Se muestra texto de usuarios como HTML? | `innerHTML`, `dangerouslySetInnerHTML`, `\|safe`, `mark_safe` | **No** — React escapa por defecto y no se encontró ninguno |
| ⚠ ¿Se puede ver un recurso de otro usuario cambiando el id? | Rutas `/<id>/` sin propietario | **No aplica** — no hay usuarios ni recursos con dueño |
| ⚠ ¿Las rutas de administrador solo están «ocultas» en el frontend? | Endpoints sin verificar rol | **Sí** — POST/PUT/PATCH/DELETE de libros y editoriales no exigen autenticación (`AllowAny`) |
| ⚠ ¿CORS está abierto a cualquier origen? | `CORS_ALLOW_ALL_ORIGINS` | **Sí** — `CORS_ALLOW_ALL_ORIGINS = True` |
| ⚠ ¿El proyecto usa HTTP simple? | URL de acceso | **Sí** — `http://127.0.0.1:8000` y `http://localhost:3000` |

Revisión de `settings.py`: `DEBUG = True` (**sí**), `ALLOWED_HOSTS = []` (vacío; no es `['*']`, pero falla en producción), `SECRET_KEY` escrita en el archivo y con prefijo `django-insecure-` (**sí**).

`python manage.py check --deploy` → **7 problemas** (1 error + 6 advertencias): `mail.E001`, `W004` (HSTS), `W008` (SSL redirect), `W009` (SECRET_KEY insegura), `W016` (CSRF cookie no Secure), `W018` (DEBUG), `W020` (ALLOWED_HOSTS).

## Hallazgos

| # | Hallazgo | OWASP | Evidencia (cómo lo comprobé) | Corrección aplicada | Estado |
|---|----------|-------|------------------------------|---------------------|--------|
| 1 | `SECRET_KEY` escrita en `settings.py` y subida al repositorio | A04 / A02 | `devconf/settings.py`; `check --deploy` → W009 | | Pendiente |
| 2 | Endpoints de escritura sin autenticación ni rol | A01 | `REST_FRAMEWORK` con `AllowAny` y sin autenticación; cualquiera puede crear, editar o borrar libros y editoriales | | Pendiente |
| 3 | CORS abierto a cualquier origen | A02 | `curl -I -H "Origin: https://evil.example" /api/libros/` → `access-control-allow-origin: *` | | Pendiente |
| 4 | `DEBUG = True` fijo en el código | A02 | `settings.py`; `check --deploy` → W018 | | Pendiente |
| 5 | Tráfico por HTTP sin cifrar, sin HSTS ni cookies Secure | A04 | Se accede por `http://`; W004, W008, W016 | | Pendiente |
| 6 | `ALLOWED_HOSTS` vacío | A02 | `check --deploy` → W020 | | Pendiente |
| 7 | Sin sistema de usuarios, login ni límite de intentos | A07 | No existe `django.contrib.auth` en `INSTALLED_APPS` ni rutas de login | | Pendiente |
