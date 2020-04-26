from django.urls import path
from .views import ShareListView, ShareDetailView

urlpatterns = [
    path('', ShareListView.as_view(), name='home'),
    path('share/<int:pk>/', ShareDetailView.as_view(), name='share_detail')
]
