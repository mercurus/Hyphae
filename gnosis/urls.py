from django.urls import path, re_path
from . import views

app_name = 'gnosis'
urlpatterns = [
    path('', views.spa_entrance, name='spa_entrance'),
    re_path(r'(?P<url>.+)', views.catchall), #redirect to spa_entrance
]
