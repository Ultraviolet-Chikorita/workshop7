from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('process-name/', views.processName, name='process_name'),
    path('.well-known/farcaster.json', views.farcaster_manifest_view, name='farcaster-manifest'),
    path('api/webhook', views.webhook_view, name='webhook'),
]
