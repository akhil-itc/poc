from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'),
         name='login'),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('api/', include('userAuth.api.urls'), name="rest-api"),
    # path('profile/<pk>',views.ProfileView.as_view(),name = "profile")
]
