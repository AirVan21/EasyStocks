from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Share, CurrencyInstrument, Article


class ShareListView(ListView):
    model = Share
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(ShareListView, self).get_context_data(**kwargs)
        context['share_list'] = Share.objects.all()
        context['currency_list'] = CurrencyInstrument.objects.all()
        context['share_rus'] = list(filter(lambda item: item.countryCode == 'RUS',
                                           Share.objects.all()))
        context['share_usa'] = list(filter(lambda item: item.countryCode == 'USA',
                                           Share.objects.all()))
        context['tech'] = list(filter(lambda item: item.sector == 'tech',
                                      Share.objects.all()))
        context['materials'] = list(filter(lambda item: item.sector == 'materials',
                                           Share.objects.all()))
        return context


class ShareDetailView(DetailView):
    model = Share
    template_name = 'share_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ShareDetailView, self).get_context_data(**kwargs)
        context['news'] = Article.objects.filter(share=self.object)
        return context
