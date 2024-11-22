"""
URL configuration for registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePage,name= 'home'),
    path('signup/',views.SignUpPage,name='signup' ),
    path('login/',views.LoginPage, name='login'),
    path('logout/',views.LogOut,name='logout'),
    path('about/',views.About,name='about'),
    path('otp/',views.otp_view,name='otp'),
    # path('forget-password/',views.ForgetPassword,name="forget_password"),
    # path('change-password/<token>/',views.ChangePassword,name="change_password"),
    
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='forget-password.html'),name ="password_reset"),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name ="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name ="password_reset_confirm"),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name ="password_reset_complete"),
    
]


