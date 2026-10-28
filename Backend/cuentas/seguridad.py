import datetime
from functools import wraps

import jwt
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.middleware.csrf import CsrfViewMiddleware


def rol_de(user):
    return 'admin' if user.is_staff else 'cliente'


def crear_token(user):
    ahora = datetime.datetime.now(datetime.timezone.utc)
    return jwt.encode(
        {'sub': str(user.pk), 'rol': rol_de(user), 'exp': ahora + datetime.timedelta(minutes=15)},
        settings.JWT_SECRET, algorithm='HS256')


def _clave_intentos(request):
    return 'login:' + request.META.get('REMOTE_ADDR', '?')


def limitado(request, maximo=5):
    return cache.get(_clave_intentos(request), 0) >= maximo


def registrar_fallo(request, ventana=900):
    # solo cuentan los intentos fallidos: un login correcto no bloquea al usuario
    clave = _clave_intentos(request)
    cache.add(clave, 0, ventana)
    cache.incr(clave)


def _falla_csrf(request):
    # Django REST marca sus vistas como csrf_exempt: se repite aquí la comprobación
    # de Django (cookie csrftoken = cabecera X-CSRFToken y origen de confianza)
    django_request = getattr(request, '_request', request)
    if django_request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
        return None
    django_request.csrf_processing_done = False
    return CsrfViewMiddleware(lambda r: None).process_view(django_request, None, (), {})


def autenticado(rol=None):
    def deco(vista):
        @wraps(vista)
        def interna(request, *args, **kwargs):
            try:
                datos = jwt.decode(request.COOKIES.get('token', ''),
                                   settings.JWT_SECRET, algorithms=['HS256'],
                                   options={'require': ['exp', 'sub']})
            except jwt.PyJWTError:
                return JsonResponse({'error': 'No autenticado'}, status=401)
            if rol and datos.get('rol') != rol:
                return JsonResponse({'error': 'Sin permiso'}, status=403)
            if _falla_csrf(request) is not None:
                return JsonResponse({'error': 'Token CSRF inválido'}, status=403)
            request.usuario_id = datos['sub']  # ObjectId de MongoDB como texto
            request.rol = datos['rol']
            return vista(request, *args, **kwargs)
        return interna
    return deco
