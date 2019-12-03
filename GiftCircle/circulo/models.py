from django.db import models

# Create your models here.

class Circulo(models.Model):
    nombre    = models.CharField(max_length=200)
    shuffeled = models.BooleanField()

    def __str__(self):
        return self.nombre


class Persona(models.Model):
    circulo  = models.ForeignKey(Circulo, on_delete=models.CASCADE)
    nombre   = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    email    = models.EmailField()

    def __str__(self):
        return self.nombre

    @classmethod
    def create(cls, nombre, telefono="", email=""):
        persona = cls(nombre=nombre, telefono=telefono, email=email)
        return persona


class Deseo(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    deseo   = models.CharField(max_length=200)

    def __str__(self):
        return self.deseo
