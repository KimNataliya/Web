from django.db import models
import datetime
from django.urls import reverse


from django.contrib.auth.models import User

from datetime import date

class Food(models.Model):
    name = models.CharField(max_length=200, null=False)
    quantity = models.PositiveIntegerField(null=False, default=0)
    calorie = models.FloatField(null=False, default=0)
    proteins = models.FloatField(default=0)
    fats = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    person_of = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Profile(models.Model):
    person_of = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    calorie_count = models.FloatField(default=0, null=True, blank=True)
    proteins_count = models.FloatField(default=0)
    fats_count = models.FloatField(default=0)
    carbs_count = models.FloatField(default=0)
    food_selected = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.FloatField(default=0)
    total_calorie = models.FloatField(default=0, null=True)
    total_proteins = models.FloatField(default=0, null=True)
    total_fats = models.FloatField(default=0, null=True)
    total_carbs = models.FloatField(default=0, null=True)
    date = models.DateField(auto_now_add=True)
    calorie_goal = models.PositiveIntegerField(default=0)
    proteins_goal = models.PositiveIntegerField(default=0)  # Цель по белкам
    fats_goal = models.PositiveIntegerField(default=0)  # Цель по жирам
    carbs_goal = models.PositiveIntegerField(default=0)  # Цель по углеводам
    all_food_selected_today = models.ManyToManyField(Food, through='PostFood', related_name='inventory')

    def save(self, *args, **kwargs):  # new
        if self.food_selected != None:
            self.amount_calorie = (self.food_selected.calorie / self.food_selected.quantity)
            self.amount_proteins = (self.food_selected.proteins / self.food_selected.quantity)
            self.amount_fats = (self.food_selected.fats / self.food_selected.quantity)
            self.amount_carbs = (self.food_selected.carbs / self.food_selected.quantity)

            self.calorie_count = self.amount_calorie * self.quantity
            self.proteins_count = self.amount_proteins * self.quantity
            self.fats_count = self.amount_fats * self.quantity
            self.carbs_count = self.amount_carbs * self.quantity

            self.total_calorie = self.calorie_count + self.total_calorie
            self.total_proteins = self.proteins_count + self.total_proteins
            self.total_fats = self.fats_count + self.total_fats
            self.total_carbs = self.carbs_count + self.total_carbs

            calories = Profile.objects.filter(person_of=self.person_of).last()

            PostFood.objects.create(profile=calories, food=self.food_selected, calorie_amount=self.calorie_count,
                                    proteins_amount=self.proteins_count, fats_amount=self.fats_count,
                                    carbs_amount=self.carbs_count, amount=self.quantity)
            self.food_selected = None
            super(Profile, self).save(*args, **kwargs)
        else:
            super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.person_of.username)


class PostFood(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    calorie_amount = models.FloatField(default=0, null=True, blank=True)
    proteins_amount = models.FloatField(default=0, null=True, blank=True)
    fats_amount = models.FloatField(default=0, null=True, blank=True)
    carbs_amount = models.FloatField(default=0, null=True, blank=True)
    amount = models.FloatField(default=0)
