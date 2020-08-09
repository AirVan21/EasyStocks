from django.contrib.auth.models import User
from django.db import models


class Person(User):

    class Meta:
        proxy = True


class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    shares = models.ManyToManyField('stocks.Share')

    def __str__(self):
        return self.title
