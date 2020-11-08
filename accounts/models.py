from django.contrib.auth.models import User
from django.db import models


class Person(User):

    class Meta:
        proxy = True


class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    shares = models.ManyToManyField(
        'stocks.Share'
    )

    def __str__(self):
        return ' '.join([self.owner.__str__(), self.title])
