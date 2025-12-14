from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('process-name/', views.processName, name='process_name'),
]