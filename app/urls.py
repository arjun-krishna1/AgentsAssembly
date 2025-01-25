from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('agent-settings/', views.agent_settings, name='agent_settings'),
    path('create-bill/', views.create_bill, name='create_bill'),
    # API endpoints
    path('api/bills/', views.get_bills, name='get_bills'),
    path('api/bills/<int:bill_id>/vote/', views.vote_on_bill, name='vote_on_bill'),
]