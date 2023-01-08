from django.urls import path, include
from . import views

app_name = 'conduct'
urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),

    # path('user/', include('django.contrib.auth.urls')), #https://github.com/django/django/blob/master/django/contrib/auth/urls.py
    path('profile', views.profile, name='profile'),
]
