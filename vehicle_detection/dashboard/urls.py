from django.urls import path
from . import views

urlpatterns = [
      path('', views.video_upload_view, name='video_upload'),
      path('vehicles/', views.vehicle_list, name='vehicle_list'),
]
