from django.urls import path

from .views import ShareListView, ShareDetailView

urlpatterns = [
    path('', ShareListView.as_view(), name='home'),
]