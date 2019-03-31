from django.db import models

class Share(models.Model):
    title = models.CharField(max_length=200)
    ticker = models.CharField(max_length=10)
    text = models.TextField()

    def __str__(self):
        return self.title
