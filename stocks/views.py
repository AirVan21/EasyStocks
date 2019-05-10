from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Share

class ShareListView(ListView):
    model = Share
    template_name = 'home.html'


class ShareDetailView(DetailView):
    model = Share
    template_name = 'share_detail.html'
