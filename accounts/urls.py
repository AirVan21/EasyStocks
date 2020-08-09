from django.urls import path
from .views import SignUpView, PersonDetailView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path(
        'person/<int:person_id>/add_share/<int:share_id>/',
        PersonDetailView.add_share,
        name='add_share'
    ),
    path('person/<int:pk>/', PersonDetailView.as_view(), name='personal'),
]
