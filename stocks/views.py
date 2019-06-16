from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Share, CurrencyInstrument

class ShareListView(ListView):
    model = Share
    template_name = 'home.html'


    def get_context_data(self, **kwargs):
        context = super(ShareListView, self).get_context_data(**kwargs)
        context['share_list'] = Share.objects.all()
        context['currency_list'] = CurrencyInstrument.objects.all()
        return context


class ShareDetailView(DetailView):
    model = Share
    template_name = 'share_detail.html'
