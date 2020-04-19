from django.db import models
from django.utils.timezone import now


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
    dataProvider = models.ForeignKey(
        'MarketDataProvider',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    competitors = models.ManyToManyField('Share')

    def __str__(self):
        return self.title


class ShareDataItem(models.Model):
    share = models.ForeignKey(
        'Share',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    date = models.DateField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.FloatField()


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
    share = models.ForeignKey(
        'Share',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.title

    @staticmethod
    def are_valid_arguments(article_dict):
        if not article_dict['author']:
            return False
        if not article_dict['title']:
            return False
        if not article_dict['description']:
            return False
        if not article_dict['url']:
            return False
        if not article_dict['urlToImage']:
            return False
        if not article_dict['content']:
            return False
        return True

    @staticmethod
    def get_source_name(article_dict):
        source = article_dict['source']
        return source['name']


class Dividend(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    share = models.ForeignKey(
        'Share',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.date


class Product(models.Model):
    name = models.CharField(max_length=200, blank=True)
    revenue = models.IntegerField()
    date = models.DateField(default=now)
    share = models.ForeignKey(
        'Share',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.name


class Indicators(models.Model):
    revenue = models.IntegerField()
    earnings = models.IntegerField()
    date = models.DateField(default=now)
    share = models.ForeignKey(
        'Share',
        on_delete=models.CASCADE,
        null=True
    )


class Customer(models.Model):
    location = models.CharField(max_length=200, blank=True)
    percentage = models.IntegerField()
    date = models.DateField(default=now)
    share = models.ForeignKey(
        'Share',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.location
