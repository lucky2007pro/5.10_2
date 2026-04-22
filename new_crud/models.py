from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'auth_user'

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    desc = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)