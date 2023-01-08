from django.urls import path
from . import views
from . import endpoints

app_name = 'gnosis'
urlpatterns = [
    path('list_morphs', endpoints.list_morphs, name='list_morphs'),
    path('list_topics', endpoints.list_topics, name='list_topics'),
    


    # path('morphs', views.MorphSearch.as_view(), name='morph_search'),
    # path('morphs/create', views.MorphCreate.as_view(), name='morph_create'),
    # path('morphs/<int:pk>', views.MorphEdit.as_view(), name='morph_edit'),
    
    # path('catalog', views.catalog, name='catalog'),
    # path('relate', views.relate, name='relate'),
    # path('unrelate', views.unrelate, name='unrelate'),
    
    # path('topics', views.TopicSearch.as_view(), name='topic_search'),
    # path('topics/create/<int:morph_id>', views.TopicCreate.as_view(), name='topic_create'),
    # path('topics/<int:pk>', views.TopicDetails.as_view(), name='topic_details'),
    # path('topics/<int:pk>/edit', views.TopicEdit.as_view(), name='topic_edit'),
    
    # path('folks', views.FolkSearch.as_view(), name='folk_search'),
    # path('folks/create/<int:morph_id>', views.FolkCreate.as_view(), name='folk_create'),
    # path('folks/<int:pk>', views.FolkDetails.as_view(), name='folk_details'),
    # path('folks/<int:pk>/edit', views.FolkEdit.as_view(), name='folk_edit'),
    
    # path('notes', views.NoteSearch.as_view(), name='note_search'),
    # path('notes/create/<int:morph_id>', views.NoteCreate.as_view(), name='note_create'),
    # path('notes/<int:pk>', views.NoteDetails.as_view(), name='note_details'),
    # path('notes/<int:pk>/edit', views.NoteEdit.as_view(), name='note_edit'),
    
    # path('creations', views.CreationSearch.as_view(), name='creation_search'),
    # path('creations/create/<int:morph_id>', views.CreationCreate.as_view(), name='creation_create'),
    # path('creations/<int:pk>', views.CreationDetails.as_view(), name='creation_details'),
    
]
