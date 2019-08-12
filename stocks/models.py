from django.db import models


class MarketDataProvider(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    folder = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Share(models.Model):
    title = models.CharField(max_length=200)
    ticker = models.CharField(max_length=10)
    text = models.TextField()
    countryCode = models.CharField(max_length=3)
    sector = models.CharField(max_length=30)
    dataProvider = models.ForeignKey('MarketDataProvider',
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True)

    def __str__(self):
        return self.title


class CurrencyInstrument(models.Model):
    title = models.CharField(max_length=200)
    ticker = models.CharField(max_length=10)
    base_currency = models.CharField(max_length=10)
    instrument_currency = models.CharField(max_length=10)
    text = models.TextField()

    def __str__(self):
        return self.title


class Article(models.Model):
    author = models.CharField(max_length=200, blank=True)
    title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    url_to_image = models.URLField(blank=True)
    content = models.TextField(blank=True)
    publish_dateTime = models.DateTimeField(blank=True)
    share = models.ForeignKey('Share',
                              on_delete=models.CASCADE,
                              null=True)

    def __str__(self):
        return self.title
