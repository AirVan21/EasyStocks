from django.views.generic import ListView, DetailView
from .models import Share, CurrencyInstrument, Article, ShareDataItem


class ShareListView(ListView):
    model = Share
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(ShareListView, self).get_context_data(**kwargs)
        context['share_list'] = Share.objects.all()
        context['currency_list'] = CurrencyInstrument.objects.all()
        context['share_rus'] = Share.objects.filter(countryCode='RUS')
        context['share_usa'] = Share.objects.filter(countryCode='USA')
        context['tech'] = Share.objects.filter(sector='tech')
        context['materials'] = Share.objects.filter(sector='materials')
        context['share_rus_trends'] = self.get_trends(context['share_rus'])
        return context

    def get_trends(self, shares):
        positive = 0
        negative = 0
        for share_item in shares:
            close_prices = ShareDataItem.objects.filter(share=share_item).values('close_price').order_by('-date')[:2]
            current, previous = close_prices[0]['close_price'], close_prices[1]['close_price']
            if (previous > current):
                negative += 1
            else:
                positive += 1
        return [positive, negative]


class ShareDetailView(DetailView):
    model = Share
    template_name = 'share_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ShareDetailView, self).get_context_data(**kwargs)
        context['news'] = Article.objects.filter(share=self.object).order_by('-publish_dateTime')
        context['chart_data'] = ShareDataItem.objects.filter(share=self.object).values('close_price', 'date', 'volume').order_by('-date')[:52]
        context['dates'] = list(map(lambda date: date['date'].strftime('%Y-%m-%d'), context['chart_data']))
        return context
