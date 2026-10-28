from rest_framework import serializers

from .models import Editorial, Libro


class EditorialSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Editorial
        fields = ("id", "nombre", "pais")


class LibroSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    editorial = EditorialSerializer(read_only=True)
    editorial_id = serializers.PrimaryKeyRelatedField(
        source="editorial",
        queryset=Editorial.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Libro
        fields = ("id", "titulo", "anio", "paginas", "imagen", "editorial", "editorial_id")


class EditorialDetailSerializer(EditorialSerializer):
    libros = LibroSerializer(many=True, read_only=True)

    class Meta:
        model = Editorial
        fields = ("id", "nombre", "pais", "libros")