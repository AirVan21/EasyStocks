from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views import generic
from .models import Person


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class PersonDetailView(DetailView):
    model = Person
    template_name = 'personal.html'
