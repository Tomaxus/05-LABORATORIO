from django.urls import path

from . import views

urlpatterns = [
    path("libros/", views.LibroListCreateAPIView.as_view(), name="api-libros"),
    path(
        "libros/<str:libro_id>/",
        views.LibroDetailAPIView.as_view(),
        name="api-libro-detalle",
    ),
    path("editoriales/", views.EditorialListCreateAPIView.as_view(), name="api-editoriales"),
    path(
        "editoriales/<str:editorial_id>/",
        views.EditorialDetailAPIView.as_view(),
        name="api-editorial-detalle",
    ),
]
