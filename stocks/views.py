from django.shortcuts import render
from django.views.generic import ListView

from .models import Share

class BlogListView(ListView):
    model = Share
    template_name = 'home.html'

