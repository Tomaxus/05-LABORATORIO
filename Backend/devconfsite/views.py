from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from .models import Editorial, Libro
from .serializers import EditorialDetailSerializer, EditorialSerializer, LibroSerializer


class LibroListCreateAPIView(APIView):
    @extend_schema(tags=["Libros"], responses=LibroSerializer(many=True))
    def get(self, request):
        queryset = Libro.objects.select_related("editorial").all()
        return Response(LibroSerializer(queryset, many=True).data)

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

    @extend_schema(tags=["Libros"], request=LibroSerializer, responses=LibroSerializer)
    def put(self, request, libro_id):
        libro = self._get_object(libro_id)
        if libro is None:
            return Response({"error": "Libro no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = LibroSerializer(libro, data=request.data)
        serializer.is_valid(raise_exception=True)
        libro = serializer.save()
        return Response(LibroSerializer(libro).data)

    @extend_schema(tags=["Libros"], request=LibroSerializer, responses=LibroSerializer)
    def patch(self, request, libro_id):
        libro = self._get_object(libro_id)
        if libro is None:
            return Response({"error": "Libro no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = LibroSerializer(libro, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        libro = serializer.save()
        return Response(LibroSerializer(libro).data)

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
