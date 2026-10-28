# Informe de seguridad

**Estudiantes:** Tomás Uribe Sánchez, Nicolás Rodríguez Acevedo
**Proyecto:** Backend Django + MongoDB Atlas (`Backend/`) y Frontend Next.js (`Frontend/`)
**Rama:** `seguridad`

## Parte 0 — Diagnóstico

| Pregunta | Respuesta |
|---|---|
| ¿Contraseñas guardadas tal cual? | No aplica (no hay usuarios) |
| ¿Credenciales en el código? | Sí: `SECRET_KEY` en `settings.py` |
| ¿Archivos de secretos en git? | No: `.env` está ignorado |
| ¿Texto de usuarios mostrado como HTML? | No |
| ¿Ver recursos de otro usuario cambiando el id? | No aplica |
| ¿Rutas de admin solo ocultas en el frontend? | Sí: crear, editar y borrar no piden login |
| ¿CORS abierto a cualquier origen? | Sí: `CORS_ALLOW_ALL_ORIGINS = True` |
| ¿Usa HTTP simple? | Sí |

En `settings.py`: `DEBUG = True`, `ALLOWED_HOSTS` vacío y `SECRET_KEY` escrita en el archivo.

`python manage.py check --deploy` al inicio: **7 problemas**.

## Hallazgos

| # | Hallazgo | OWASP | Evidencia | Corrección | Estado |
|---|---|---|---|---|---|
| 1 | `SECRET_KEY` en el código | A04 | `settings.py`, aviso W009 | | Pendiente |
| 2 | Crear/editar/borrar sin login | A01 | `AllowAny` en la API | | Pendiente |
| 3 | CORS abierto | A02 | Respuesta con `access-control-allow-origin: *` | | Pendiente |
| 4 | `DEBUG = True` | A02 | `settings.py`, aviso W018 | | Pendiente |
| 5 | Sin HTTPS | A04 | Se abría con `http://` | HTTPS con mkcert | Corregido |
| 6 | `ALLOWED_HOSTS` vacío | A02 | Aviso W020 | | Pendiente |
| 7 | Sin login ni límite de intentos | A07 | No hay usuarios | | Pendiente |──────────────────────────────────────────────────────────────────────────────────────────────────────


## Parte 1 — HTTPS

Se generó un certificado local con mkcert. El backend corre en `https://localhost:8443` y el frontend en `https://localhost:3000`, con candado.

![HTTPS](evidencias/HTTPS.png)

**¿Qué garantías da HTTPS que HTTP no da? ¿Garantiza que el sitio sea honesto?**
Da **cifrado** (nadie puede leer los datos en el camino) e **integridad** (nadie puede cambiarlos, y el certificado confirma el dominio). No garantiza que el sitio sea honesto: una página falsa también puede tener candado.
