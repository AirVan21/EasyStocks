from django.contrib import admin
from .models import Share, CurrencyInstrument, MarketDataProvider, Article, ShareDataItem


admin.site.register(Share)
admin.site.register(CurrencyInstrument)
admin.site.register(MarketDataProvider)
admin.site.register(Article)
admin.site.register(ShareDataItem)
