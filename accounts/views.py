from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views import generic
from .models import Person, Portfolio
from stocks.models import Share


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class PersonDetailView(DetailView):
    model = Person
    template_name = 'personal.html'

    def get_context_data(self, **kwargs):
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        portfolioQuery = Portfolio.objects.filter(owner=self.object)
        if portfolioQuery:
            portfolio = portfolioQuery[0]
            context['portfolio_shares'] = portfolio.shares.all()
        return context

    @staticmethod
    def add_share(request, person_id, share_id):
        if request.method == 'POST':
            person = Person.objects.get(pk=person_id)
            share = Share.objects.get(pk=share_id)
            portfolioQuery = Portfolio.objects.filter(owner=person_id)
            if portfolioQuery:
                portfolio = portfolioQuery[0]
                portfolio.shares.add(share)
                portfolio.save()
            else:
                portfolio = Portfolio(
                    title='General',
                    owner=person
                )
                portfolio.save()
                portfolio.shares.add(share)
                portfolio.save()
        return redirect('/')
