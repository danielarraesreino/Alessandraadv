from django.urls import path
from . import views

app_name = 'admin_portal'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('leads/', views.leads_kanban, name='leads_kanban'),
    path('leads/<int:lead_id>/', views.lead_detail, name='lead_detail'),
    path('leads/<int:lead_id>/convert/', views.convert_lead, name='convert_lead'),
    
    # Clients
    path('clients/', views.clients_list, name='clients_list'),
    path('clients/<int:client_id>/', views.client_detail, name='client_detail'),
    path('clients/<int:client_id>/edit/', views.client_edit, name='client_edit'),
    path('clients/create/', views.client_create, name='client_create'),
    
    # Cases
    path('cases/', views.cases_kanban, name='cases_kanban'),
    path('cases/<int:case_id>/', views.case_detail, name='case_detail'),
    path('cases/<int:case_id>/edit/', views.case_edit, name='case_edit'),
    path('cases/create/', views.case_create, name='case_create'),
    
    # Finance
    path('finance/', views.finance_list, name='finance_list'),
    path('finance/create/', views.finance_create, name='finance_create'),
    path('finance/<int:item_id>/pay/', views.finance_pay, name='finance_pay'),
]
