from django.urls import path
from . import views
urlpatterns = [

    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('loginpage', views.login_page, name='login'),
    path('user-settings', views.user_settings, name='user_settings'),
    path('user-logout', views.user_logout, name='logout'),
    path('delete-account', views.account_delete, name='delete_account'),
    path('already-logged', views.already_logged, name='already_logged')

]