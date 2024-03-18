from django.db import models


class User(models.Model):
    email = models.CharField(max_length=30)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20)
