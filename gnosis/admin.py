from django.contrib import admin
from .models import *

admin.site.register(Morph)
admin.site.register(MorphScript)
admin.site.register(Note)
admin.site.register(Topic)
admin.site.register(TopicRelation)
admin.site.register(TopicMorph)
admin.site.register(TopicNote)
