import datetime

from django.db import models

from config.settings import AUTH_USER_MODEL

User = AUTH_USER_MODEL


# Create your models here.
class Ingredient(models.Model):
    STATE_CHOICES = (
        ('freeze', 'freeze'),
        ('cold', 'cold'),
    )

    name = models.CharField(max_length=30)
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    shelf_life = models.IntegerField()  # 유통기한


class Refrigerator(models.Model):
    ingredients = models.ManyToManyField(Ingredient, through='MyIngredientInfo')


# 중간모델 사용해서 구매일, 양 저장
class MyIngredientInfo(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    refrigerator = models.ForeignKey(Refrigerator, on_delete=models.CASCADE)
    buy_date = models.DateField(default=datetime.date.today)
    quantity = models.CharField(max_length=30)

    def left_days(self):
        shelf_life = self.ingredient.shelf_life
        keeping_date = self.buy_date + datetime.timedelta(days=shelf_life)
        left = keeping_date - datetime.datetime.today().date()
        left_days = left.days

        if shelf_life - left_days > shelf_life:
            return -left_days
        return left_days
