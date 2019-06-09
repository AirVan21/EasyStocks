from django.contrib import admin
from .models import Share, CurrencyInstrument

admin.site.register(Share)
admin.site.register(CurrencyInstrument)