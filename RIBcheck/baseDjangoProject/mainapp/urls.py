from django.urls import path
from django.contrib import admin
from . import views

app_name = 'mainapp'

urlpatterns = [
  path('', views.index, name='index'),
  path('login/', views.login_request, name='login'),
  path("logout/", views.logout_request, name="logout"),
  path("profile/", views.profile, name="profile"),
  path('register/', views.register_request, name='register'),
]