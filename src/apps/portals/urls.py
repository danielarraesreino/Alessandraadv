from django.urls import path
from . import views

app_name = 'portals'

urlpatterns = [
    path('timeline/', views.portal_timeline, name='portal_timeline'),
]
