from django.db import models

class Share(models.Model):
    title = models.CharField(max_length=200)
    ticker = models.CharField(max_length=10)
    text = models.TextField()

    def __str__(self):
        return self.title


class CurrencyInstrument(models.Model):
    title = models.CharField(max_length=200)
    ticker = models.CharField(max_length=10)
    base_currency = models.CharField(max_length=10)
    instrument_curremcy = models.CharField(max_length=10)
    text = models.TextField()

    def __str__(self):
        return self.title