from django.urls import path
from . import views

app_name = 'portals'

urlpatterns = [
    path('timeline/', views.portal_timeline, name='portal_timeline'),
    path('api/timeline-fragment/<str:token>/', views.timeline_fragment, name='timeline_fragment'),
    path('api/documents-fragment/<str:token>/', views.documents_fragment, name='documents_fragment'),
]
