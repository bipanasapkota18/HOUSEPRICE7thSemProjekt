from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('password-reset/<username>/', views.password_reset, name='password_reset'),
    # path('download-history/', views.generate_pdf, name='download_history'),

]