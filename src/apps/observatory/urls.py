from django.urls import path
from . import views

app_name = 'observatory'

urlpatterns = [
    path('', views.observatory_dashboard, name='dashboard'),
]
