from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField


class Editorial(models.Model):
    id = ObjectIdAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)

    class Meta:
        db_table = "libros_editorial"

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    id = ObjectIdAutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    anio = models.PositiveIntegerField()
    paginas = models.PositiveIntegerField()
    imagen = models.CharField(max_length=200)
    editorial = models.ForeignKey(
        Editorial,
        on_delete=models.CASCADE,
        related_name="libros",
    )

    class Meta:
        db_table = "libros_libro"

    def __str__(self):
        return self.titulo
