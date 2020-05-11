from django.contrib.auth.models import User


class Person(User):

    class Meta:
        proxy = True
