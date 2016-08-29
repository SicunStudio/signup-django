from django.db import models


# Create your models here.
class Config(models.Model):
    name = models.TextField(null=False)
    value = models.TextField(null=False)
