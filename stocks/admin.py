from django.contrib import admin
from .models import (
    Share,
    CurrencyInstrument,
    MarketDataProvider,
    Article,
    ShareDataItem,
    Dividend,
    Product,
    Indicators,
    Customer,
    Currency
)


admin.site.register(Share)
admin.site.register(CurrencyInstrument)
admin.site.register(MarketDataProvider)
admin.site.register(Article)
admin.site.register(ShareDataItem)
admin.site.register(Dividend)
admin.site.register(Product)
admin.site.register(Indicators)
admin.site.register(Customer)
admin.site.register(Currency)
