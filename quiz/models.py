from django.db import models

# Create your models here.


class Staff(models.Model):
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=10)
