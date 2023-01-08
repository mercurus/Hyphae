import json
from django.db import models
from django.contrib.auth.models import User


FIELD_TYPES = [
    'text',
    'bigtext',
    'number',
    'date',
]


class Morph(models.Model):
    """Schema for the data associated with an Topic"""
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50) #CSS class for FontAwesome
    json_data = models.JSONField(blank=True)
    def __str__(self): 
        return self.name

    def is_json_valid(self, json_obj):
        if not type(json_obj) is dict:
            if type(json_obj) is str:
                try:
                    json_obj = json.loads(json_obj)
                except json.JSONDecodeError:
                    print('decode error')
                    return False
            return False

        #ok, argument was a dict so now compare keys/values against template
        # print(type(self.json_data))
        # print(self.json_data)
        # print(self.json_data['fields'])
        field_names = [ obj['name'] for obj in self.json_data['fields'] ]
        for key, value in json_obj.items():
            if key not in field_names:
                print(key, value, 'not in template')
                return False
            # field = self.json_data[key]
            # if field.type == 'string':
            #     if not type(value) is str:
            #         pass
        
        return True


class MorphScript(models.Model):
    """Javascript for customizing the behavior of a Morph"""
    morph = models.ForeignKey(Morph, on_delete=models.CASCADE, related_name='scripts')
    filename = models.CharField(max_length=100)


class Topic(models.Model):
    """Some thing that can be linked to other things and discussed"""
    # FOLK = 1
    # TOPIC = 2
    # KINDS = [
    #     (FOLK, 'Folk'),
    #     (TOPIC, 'Topic'),
    # ]
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, blank=True) #CSS icon class
    json_data = models.JSONField(blank=True)
    morph = models.ForeignKey(Morph, on_delete=models.SET_NULL, null=True) #primary
    # kind = models.PositiveSmallIntegerField(choices=KINDS, default=FOLK)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_elements')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_elements')
    created_date = models.DateTimeField(auto_now_add=True)
    # modified_date = models.DateTimeField(auto_now=True)
    # modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, related_name='modified_elements')
    def __str__(self): 
        return self.name


# class TopicHistory(models.Model):
#     """Edit history record of an topic"""
#     topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)
#     morph = models.ForeignKey(Morph, on_delete=models.SET_NULL, null=True)
#     json_data = models.JSONField(blank=True)
#     modified_date = models.DateTimeField(auto_now_add=True)
#     modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
#     def __str__(self): 
#         return self.name


class TopicRelation(models.Model):
    """M2M Topics"""
    parent = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='children')
    child = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='parents')
    json_data = models.JSONField(blank=True)
    def __str__(self): 
        return self.json_data[:50]


class TopicMorph(models.Model):
    """M2M secondary morphs"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    morph = models.ForeignKey(Morph, on_delete=models.CASCADE)
    # json_data = models.JSONField(blank=True)
    # def __str__(self): 
    #     return self.json_data[:50]


class Note(models.Model):
    """Forum post, comment, or other communication post"""
    # name = models.CharField(max_length=250)
    text = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True) #CSS class
    json_data = models.JSONField(blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    # morph = models.ForeignKey(Morph, on_delete=models.SET_NULL, null=True)
    # ancestor = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='grandchildren')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='children')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    # modified_date = models.DateTimeField(auto_now=True)
    def __str__(self): 
        return self.name


class TopicNote(models.Model):
    """Discussions related to an Topic"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    # json_data = models.JSONField(blank=True)
    def __str__(self): 
        # return self.json_data[:50]
        return ''


##############################################
##==||    ||==##
##############################################















# # FOLKS


# class Folk(models.Model):
#     """People (users) or groups of people"""
#     morph = models.ForeignKey(Morph, on_delete=models.SET_NULL, null=True)
#     name = models.CharField(max_length=50)
#     json = models.JSONField()
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, related_name='old_folk')
#     icon = models.CharField(max_length=50, blank=True) #FontAwesome
#     topics = models.ManyToManyField('Topic', through='FolkTopic', blank=True)
#     notes = models.ManyToManyField('Note', through='FolkNote', blank=True)
#     # created_date = models.DateTimeField(auto_now_add=True)
#     # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
#     def __str__(self): 
#         return self.name


# class FolkFolk(models.Model):
#     """M2M"""
#     parent = models.ForeignKey(Folk, on_delete=models.SET_NULL, null=True, related_name='children')
#     child = models.ForeignKey(Folk, on_delete=models.SET_NULL, null=True, related_name='parents')
#     json = models.JSONField(blank=True)
#     def __str__(self): 
#         return self.json[:50]


# class FolkMorph(models.Model):
#     """M2M secondary morphs"""
#     folk = models.ForeignKey(Folk, on_delete=models.SET_NULL, null=True)
#     morph = models.ForeignKey(Morph, on_delete=models.SET_NULL, null=True)
#     json = models.JSONField(blank=True)
#     def __str__(self): 
#         return self.json[:50]


# # TOPICS


# class Topic(models.Model):
#     """A concept, idea, or blueprint"""
#     name = models.CharField(max_length=50)
#     morph = models.ForeignKey(Morph, on_delete=models.SET_NULL, null=True)
#     json = models.JSONField(blank=True)
#     icon = models.CharField(max_length=50, blank=True) #CSS icon
#     folks = models.ManyToManyField('Folk', through='FolkTopic', blank=True)
#     notes = models.ManyToManyField('Note', through='TopicNote', blank=True)
#     # created_date = models.DateTimeField(auto_now_add=True)
#     # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
#     def __str__(self): 
#         return self.name


# class TopicTopic(models.Model):
#     """M2M"""
#     parent = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, related_name='children')
#     child = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, related_name='parents')
#     json = models.JSONField(blank=True)
#     def __str__(self): 
#         return self.json[:50]


# class TopicMorph(models.Model):
#     """M2M secondary morphs"""
#     topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
#     morph = models.ForeignKey(Morph, on_delete=models.SET_NULL, null=True)
#     json = models.JSONField(blank=True)
#     def __str__(self): 
#         return self.json[:50]


# # NOTES


# class Note(models.Model):
#     """Words communicated or recorded"""
#     name = models.CharField(max_length=50)
#     morph = models.ForeignKey(Morph, on_delete=models.SET_NULL, null=True)
#     json = models.JSONField(blank=True)
#     icon = models.CharField(max_length=50, blank=True) #FontAwesome
#     folks = models.ManyToManyField('Folk', through='FolkNote', blank=True)
#     topics = models.ManyToManyField('Topic', through='TopicNote', blank=True)
#     # created_date = models.DateTimeField(auto_now_add=True)
#     # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
#     def __str__(self): 
#         return self.name


# class NoteNote(models.Model):
#     """M2M"""
#     parent = models.ForeignKey(Note, on_delete=models.SET_NULL, null=True, related_name='children')
#     child = models.ForeignKey(Note, on_delete=models.SET_NULL, null=True, related_name='parents')
#     json = models.JSONField(blank=True)
#     def __str__(self): 
#         return self.json[:50]


# class NoteMorph(models.Model):
#     """M2M secondary morphs"""
#     note = models.ForeignKey(Note, on_delete=models.SET_NULL, null=True)
#     morph = models.ForeignKey(Morph, on_delete=models.SET_NULL, null=True)
#     json = models.JSONField(blank=True)
#     def __str__(self): 
#         return self.json[:50]


# ################################################
# ##==||  OUTER MANY TO MANY RELATIONSHIPS  ||==##
# ################################################


# class FolkTopic(models.Model):
#     """M2M"""
#     folk = models.ForeignKey(Folk, on_delete=models.SET_NULL, null=True)
#     topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
#     json = models.JSONField(blank=True)
#     def __str__(self): 
#         return self.json[:50]


# class FolkNote(models.Model):
#     """M2M"""
#     folk = models.ForeignKey(Folk, on_delete=models.SET_NULL, null=True)
#     note = models.ForeignKey(Note, on_delete=models.SET_NULL, null=True)
#     json = models.JSONField(blank=True)
#     def __str__(self): 
#         return self.json[:50]


# class TopicNote(models.Model):
#     """M2M"""
#     topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
#     note = models.ForeignKey(Note, on_delete=models.SET_NULL, null=True)
#     json = models.JSONField(blank=True)
#     def __str__(self): 
#         return self.json[:50]



