from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/auth/", include("cuentas.urls")),
    path("api/", include("devconfsite.urls")),
]


# Respuesta genérica cuando DEBUG está apagado: sin rutas ni trazas
def error_500(request):
    return JsonResponse({"error": "Error interno"}, status=500)


def error_404(request, exception):
    return JsonResponse({"error": "No encontrado"}, status=404)


handler500 = error_500
handler404 = error_404
