from django.contrib import admin
from .models import Share, CurrencyInstrument, MarketDataProvider


admin.site.register(Share)
admin.site.register(CurrencyInstrument)
admin.site.register(MarketDataProvider)