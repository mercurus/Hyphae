# from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *


def list_morphs(request):
    morphs = list(Morph.objects.all().values())
    return JsonResponse({ 'records':morphs })


def list_topics(request):
    topics = list(Topic.objects.all().values())
    return JsonResponse({ 'records':topics })
