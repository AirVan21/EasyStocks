from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from .models import (
    Share,
    CurrencyInstrument,
    Article,
    ShareDataItem,
    Product,
    Customer,
    Currency,
    Indicators,
    Dividend
)


class ShareListView(ListView):
    model = Share
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(ShareListView, self).get_context_data(**kwargs)
        context['share_list'] = Share.objects.all()
        context['currency_list'] = CurrencyInstrument.objects.all()
        context['news_list'] = Article.objects.all()
        context['share_rus'] = Share.objects.filter(countryCode='RUS')
        context['share_usa'] = Share.objects.filter(countryCode='USA')
        context['tech_usa'] = Share.objects.filter(
            sector='tech').filter(
            countryCode='USA'
        )
        context['non_tech_usa'] = Share.objects.filter(
            countryCode='USA').exclude(
            sector='tech'
        )
        context['materials_rus'] = Share.objects.filter(
            sector='materials').filter(
            countryCode='RUS'
        )
        context['non_materials_rus'] = Share.objects.filter(
            countryCode='RUS').exclude(
            sector='materials'
        )
        context['share_rus_trends'] = self.get_trends(context['share_rus'])
        context['share_usa_trends'] = self.get_trends(context['share_usa'])
        context['dividends'] = Dividend.objects.all().order_by('-date')
        return context

    def get_trends(self, shares):
        positive = 0
        negative = 0
        for share_item in shares:
            close_prices = ShareDataItem.objects.filter(
                share=share_item).values('close_price').order_by('-date')[:2]
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
        context['news'] = Article.objects.filter(
            share=self.object).order_by('-publish_dateTime')
        context['competitors'] = self.object.competitors.all()
        chart_data = ShareDataItem.objects.filter(share=self.object).values(
            'close_price', 'date', 'volume').order_by('-date')
        context['chart_data'] = list(filter(self.is_friday_value, chart_data))[:52]
        context['dates'] = list(
            map(
                lambda date: date['date'].strftime('%Y-%m-%d'),
                context['chart_data']
            )
        )
        context['products_values'] = list(
            map(
                lambda item: item['revenue'],
                Product.objects.filter(share=self.object).filter(
                    date__year='2019').values('revenue').order_by('revenue')
            )
        )
        context['products_names'] = list(
            map(
                lambda item: item['name'],
                Product.objects.filter(share=self.object).filter(
                    date__year='2019').values('name').order_by('revenue')
            )
        )
        context['customer_percentage'] = list(
            map(
                lambda item: item['percentage'],
                Customer.objects.filter(share=self.object).filter(
                    date__year='2019').values('percentage').order_by('percentage')
            )
        )
        context['customer_locations'] = list(
            map(
                lambda item: item['location'],
                Customer.objects.filter(share=self.object).filter(
                    date__year='2019').values('location').order_by('percentage')
            )
        )
        indicators = Indicators.objects.filter(share=self.object).values(
            'revenue', 'earnings', 'date__year').order_by('date')
        context['revenue'] = list(
            map(
                lambda item: item['revenue'],
                indicators
            )
        )
        context['earnings'] = list(
            map(
                lambda item: item['earnings'],
                indicators
            )
        )
        context['indicators_years'] = list(
            map(
                lambda item: item['date__year'],
                indicators
            )
        )
        context['currency_symbol'] = self.get_currency().symbol
        return context

    def get_currency(self):
        return Currency.objects.get(id=self.object.currency.id)

    @staticmethod
    def delete_article(request, share_id, article_id):
        '''
        Deletes article from the database
        '''
        if request.method == 'POST':
            article = Article.objects.get(pk=article_id)
            article.delete()
            return redirect(''.join(['/share/', str(share_id)]))

    @staticmethod
    def is_friday_value(value):
        ''' Verifies if database item represents Friday EOD data '''
        return value['date'].weekday() == 4  # Friday
