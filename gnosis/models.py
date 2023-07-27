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
    summary = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=50) #CSS class for FontAwesome
    json_data = models.JSONField(blank=True)
    def __str__(self): 
        return self.name


class MorphScript(models.Model):
    """Javascript for customizing the behavior of a Morph"""
    morph = models.ForeignKey(Morph, on_delete=models.CASCADE, related_name='scripts')
    filename = models.CharField(max_length=100)


class Topic(models.Model):
    """Some thing that can be linked to other things and discussed"""
    name = models.CharField(max_length=50)
    summary = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=50, blank=True) #CSS icon class
    json_data = models.JSONField(blank=True)
    morph = models.ForeignKey(Morph, on_delete=models.SET_NULL, null=True) #primary
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
