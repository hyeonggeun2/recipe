from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from recipes.models import Refrigerator


class User(AbstractUser):
    name = models.CharField(max_length=30)
    refrigerator = models.OneToOneField(Refrigerator, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.refrigerator = Refrigerator.objects.create()
        super().save(*args, **kwargs)
