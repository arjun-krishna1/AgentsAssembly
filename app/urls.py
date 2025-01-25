from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('agent-settings/', views.agent_settings, name='agent_settings'),
    path('create-project/', views.create_project, name='create_project'),
]