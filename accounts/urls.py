from django.urls import path
from .views import SignUpView, PersonDetailView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('person/<int:pk>/', PersonDetailView.as_view(), name='personal')
]
