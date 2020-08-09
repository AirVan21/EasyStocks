from django.urls import path
from .views import ShareListView, ShareDetailView

urlpatterns = [
    path('', ShareListView.as_view(), name='home'),
    path('share/<int:pk>/', ShareDetailView.as_view(), name='share_detail'),
    path(
        'share/<int:share_id>/delete_article/<int:article_id>/',
        ShareDetailView.delete_article,
        name='delete_article'
    ),
]
