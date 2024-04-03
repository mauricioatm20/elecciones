from django.db import models

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    partido = models.CharField(max_length=100,
                               choices=[("Partido1", "Partido 1"), ("Partido2", "Partido 2"), ("Partido3", "Partido 3"),
                                        ("Partido4", "Partido 4")])
