from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = "student"
urlpatterns = [
    path('api/', include('student.api.urls'), name="rest-api"),
    # path('profile/<pk>',views.ProfileView.as_view(),name = "profile")
]
