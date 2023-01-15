# from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *


def list_morphs(request):
    morphs = [{
        'id': morph.id,
        'name': morph.name,
        'icon': morph.icon,
        'template': morph.json_data,
    } for morph in Morph.objects.all()]
    return JsonResponse({ 'records':morphs })


def list_topics(request):
    topics = [{
        'id': topic.id,
        'name': topic.name,
        'icon': topic.icon,
        'jsonData': topic.json_data,
        'morphId': topic.morph_id,
        'userId': topic.user_id,
        'createdById': topic.created_by_id,
        'createdDate': topic.created_date,
    } for topic in Topic.objects.all()]
    return JsonResponse({ 'records':topics })
