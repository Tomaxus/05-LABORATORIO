from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from cuentas.seguridad import autenticado

from .models import Editorial, Libro, Resena
from .serializers import (
    EditorialDetailSerializer,
    EditorialSerializer,
    LibroSerializer,
    ResenaSerializer,
)


class LibroListCreateAPIView(APIView):
    @extend_schema(tags=["Libros"], responses=LibroSerializer(many=True))
    def get(self, request):
        queryset = Libro.objects.select_related("editorial").all()
        return Response(LibroSerializer(queryset, many=True).data)

    @method_decorator(autenticado(rol="admin"))
    @extend_schema(tags=["Libros"], request=LibroSerializer, responses=LibroSerializer)
    def post(self, request):
        serializer = LibroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        libro = serializer.save()
        return Response(LibroSerializer(libro).data, status=status.HTTP_201_CREATED)


class LibroDetailAPIView(APIView):
    def _get_object(self, libro_id):
        try:
            return Libro.objects.select_related("editorial").get(pk=libro_id)
        except (Libro.DoesNotExist, ValidationError):
            return None

    @extend_schema(tags=["Libros"], responses=LibroSerializer)
    def get(self, request, libro_id):
        libro = self._get_object(libro_id)
        if libro is None:
            return Response({"error": "Libro no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(LibroSerializer(libro).data)

    @method_decorator(autenticado(rol="admin"))
    @extend_schema(tags=["Libros"], request=LibroSerializer, responses=LibroSerializer)
    def put(self, request, libro_id):
        libro = self._get_object(libro_id)
        if libro is None:
            return Response({"error": "Libro no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = LibroSerializer(libro, data=request.data)
        serializer.is_valid(raise_exception=True)
        libro = serializer.save()
        return Response(LibroSerializer(libro).data)

    @method_decorator(autenticado(rol="admin"))
    @extend_schema(tags=["Libros"], request=LibroSerializer, responses=LibroSerializer)
    def patch(self, request, libro_id):
        libro = self._get_object(libro_id)
        if libro is None:
            return Response({"error": "Libro no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = LibroSerializer(libro, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        libro = serializer.save()
        return Response(LibroSerializer(libro).data)

    @method_decorator(autenticado(rol="admin"))
    @extend_schema(tags=["Libros"], responses={204: None})
    def delete(self, request, libro_id):
        libro = self._get_object(libro_id)
        if libro is None:
            return Response({"error": "Libro no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EditorialListCreateAPIView(APIView):
    @extend_schema(tags=["Editoriales"], responses=EditorialSerializer(many=True))
    def get(self, request):
        queryset = Editorial.objects.order_by("nombre")
        return Response(EditorialSerializer(queryset, many=True).data)

    @method_decorator(autenticado(rol="admin"))
    @extend_schema(tags=["Editoriales"], request=EditorialSerializer, responses=EditorialSerializer)
    def post(self, request):
        serializer = EditorialSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        editorial = serializer.save()
        return Response(EditorialSerializer(editorial).data, status=status.HTTP_201_CREATED)


class EditorialDetailAPIView(APIView):
    def _get_object(self, editorial_id):
        try:
            return Editorial.objects.get(pk=editorial_id)
        except (Editorial.DoesNotExist, ValidationError):
            return None

    @extend_schema(tags=["Editoriales"], responses=EditorialDetailSerializer)
    def get(self, request, editorial_id):
        editorial = self._get_object(editorial_id)
        if editorial is None:
            return Response(
                {"error": "Editorial no encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(EditorialDetailSerializer(editorial).data)

    @method_decorator(autenticado(rol="admin"))
    @extend_schema(tags=["Editoriales"], request=EditorialSerializer, responses=EditorialSerializer)
    def put(self, request, editorial_id):
        editorial = self._get_object(editorial_id)
        if editorial is None:
            return Response(
                {"error": "Editorial no encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = EditorialSerializer(editorial, data=request.data)
        serializer.is_valid(raise_exception=True)
        editorial = serializer.save()
        return Response(EditorialSerializer(editorial).data)

    @method_decorator(autenticado(rol="admin"))
    @extend_schema(tags=["Editoriales"], request=EditorialSerializer, responses=EditorialSerializer)
    def patch(self, request, editorial_id):
        editorial = self._get_object(editorial_id)
        if editorial is None:
            return Response(
                {"error": "Editorial no encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = EditorialSerializer(editorial, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        editorial = serializer.save()
        return Response(EditorialSerializer(editorial).data)

    @method_decorator(autenticado(rol="admin"))
    @extend_schema(tags=["Editoriales"], responses={204: None})
    def delete(self, request, editorial_id):
        editorial = self._get_object(editorial_id)
        if editorial is None:
            return Response(
                {"error": "Editorial no encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )
        editorial.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def _resenas_visibles(request):
    # el administrador ve todas; un cliente solo las suyas
    queryset = Resena.objects.select_related("libro", "usuario")
    if request.rol == "admin":
        return queryset
    return queryset.filter(usuario_id=request.usuario_id)


class ResenaListCreateAPIView(APIView):
    @method_decorator(autenticado())
    @extend_schema(tags=["Reseñas"], responses=ResenaSerializer(many=True))
    def get(self, request):
        queryset = _resenas_visibles(request)
        libro_id = request.query_params.get("libro")
        if libro_id:
            try:
                queryset = list(queryset.filter(libro_id=libro_id))
            except ValidationError:
                queryset = []
        return Response(ResenaSerializer(queryset, many=True).data)

    @method_decorator(autenticado())
    @extend_schema(tags=["Reseñas"], request=ResenaSerializer, responses=ResenaSerializer)
    def post(self, request):
        serializer = ResenaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # el dueño sale del token, nunca del cuerpo de la petición
        resena = serializer.save(usuario_id=request.usuario_id)
        return Response(ResenaSerializer(resena).data, status=status.HTTP_201_CREATED)


class ResenaDetailAPIView(APIView):
    def _get_object(self, request, resena_id):
        try:
            return _resenas_visibles(request).get(pk=resena_id)
        except (Resena.DoesNotExist, ValidationError):
            return None

    @method_decorator(autenticado())
    @extend_schema(tags=["Reseñas"], responses=ResenaSerializer)
    def get(self, request, resena_id):
        resena = self._get_object(request, resena_id)
        if resena is None:  # 404 también si es de otro: no se revela que existe
            return Response({"error": "Reseña no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        return Response(ResenaSerializer(resena).data)

    @method_decorator(autenticado())
    @extend_schema(tags=["Reseñas"], responses={204: None})
    def delete(self, request, resena_id):
        resena = self._get_object(request, resena_id)
        if resena is None:
            return Response({"error": "Reseña no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        resena.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
