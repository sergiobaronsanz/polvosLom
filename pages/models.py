from django.db import models
from django.contrib.auth.models import User

class Firmas(models.Model):
	usuario= models.OneToOneField(User, on_delete=models.CASCADE)
	firma= models.CharField(max_length=100, verbose_name="Firma")