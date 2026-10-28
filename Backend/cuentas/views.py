import json
import logging
import re

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .seguridad import autenticado, crear_token, limitado, registrar_fallo, rol_de

logger = logging.getLogger(__name__)


def _datos(request):
    try:
        datos = json.loads(request.body or '{}')
    except ValueError:
        return {}
    return datos if isinstance(datos, dict) else {}


@require_GET
@ensure_csrf_cookie
def csrf(request):  # el frontend la llama una vez al cargar
    return JsonResponse({'ok': True})


@require_POST
def registro(request):
    d = _datos(request)
    email = str(d.get('email', '')).strip().lower()
    clave = str(d.get('clave', ''))

    if not re.match(r'^\S+@\S+\.\S+$', email) or len(clave) < 10:
        return JsonResponse({'error': 'Datos inválidos'}, status=400)
    if User.objects.filter(username=email).exists():
        return JsonResponse({'error': 'Ese correo ya está registrado'}, status=409)

    # create_user guarda el hash (PBKDF2), nunca la clave;
    # el rol lo decide el servidor: un usuario nuevo nunca es is_staff
    User.objects.create_user(username=email, email=email, password=clave)
    return JsonResponse({'ok': True}, status=201)


@require_POST
def login_view(request):
    if limitado(request):
        return JsonResponse({'error': 'Demasiados intentos, espere 15 minutos'}, status=429)
    d = _datos(request)
    email = str(d.get('email', '')).strip().lower()
    user = authenticate(request, username=email, password=str(d.get('clave', '')))
    if user is None:
        registrar_fallo(request)
        logger.warning('Login fallido para %s desde %s', email, request.META.get('REMOTE_ADDR'))
        return JsonResponse({'error': 'Usuario o contraseña incorrectos'}, status=401)

    resp = JsonResponse({'ok': True, 'rol': rol_de(user)})
    resp.set_cookie('token', crear_token(user), max_age=900,
                    httponly=True, secure=True, samesite='Strict')
    return resp


@require_POST
def logout_view(request):
    resp = JsonResponse({'ok': True})
    resp.delete_cookie('token', samesite='Strict')
    return resp


@require_GET
@autenticado()
def yo(request):  # para que el frontend sepa si hay sesión
    return JsonResponse({'id': request.usuario_id, 'rol': request.rol})
