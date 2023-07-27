from django.urls import path, include
from rest_framework import routers, urls
from .api_views import *


# router = routers.DefaultRouter()
# router.register(r'catalog_morphs', ListCreateMorphs)
# router.register(r'catalog_topics', ListTopics)


app_name = 'api'
urlpatterns = [
    # path('', include(router.urls)),
    # path('browser/', include('rest_framework.urls', namespace='rest_framework'))
    path('catalog_morphs', ListCreateMorphs.as_view()),
    path('modify_morph/<int:pk>', UpdateMorph.as_view()),
    
    path('catalog_topics', ListTopics.as_view()),
]
