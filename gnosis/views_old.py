from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.forms import modelform_factory
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from conduct.utilities import query_from_form
from .models import *
from .forms import *


class FormValidationMessagesMixin:
    """
    After a form/page is POSTed whip up a message for the user.
    Should be used with a CreateView or UpdateView
    """
    success_message = 'Successful'

    def form_valid(self, form):
        super().form_valid(form)
        message_text = self.success_message
        # if success_message wasn't set manually, look for default values based on View class
        if self.success_message == 'Successful':
            for base in self.__class__.__bases__:
                if base.__name__ == 'CreateView':
                    message_text = 'Created'
                    break
                elif base.__name__ == 'UpdateView':
                    message_text = 'Updated'
                    break
        messages.success(self.request, message_text)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        super().form_invalid(form)
        for key, val in form.errors.get_json_data().items():
            txt = ' '.join(v['message'] for v in val)
            messages.error(self.request, '{} - {}'.format(key, txt))
        return redirect(self.request.path)


class MorphMatchMixin:
    """This mixin compares the topic's JSON to its Morph's JSON template"""
    
    def post(self, request, morph_id=None, pk=None):
        # print(request.POST)
        if pk:
            topic = get_object_or_404(self.model, id=pk)
            morph = get_object_or_404(Morph, id=topic.morph.id)
            form = self.get_form_class()(request.POST, instance=topic)
        else: 
            morph = get_object_or_404(Morph, id=morph_id)
            form = self.get_form_class()(request.POST)

        if not form.is_valid():
            messages.error(self.request, 'Form is invalid')
            return redirect(request.path)

        if not morph.is_json_valid(form.cleaned_data['json_data']):
            messages.error(self.request, 'JSON is invalid')
            # print(type(form.cleaned_data['json']))
            # print(form.cleaned_data['json'])
            return redirect(request.path)

        messages.success(self.request, 'Saved')
        self.object = form.save()
        return redirect(self.get_success_url())


class SimpleSearchMixin:
    def get_queryset(self):
        # model_form = modelform_factory(Folk, exclude=[''])
        form = TopicForm(self.request.GET)
        fields = {
            'id': 'id',
            'name__icontains': 'name',
            'morph': 'morph',
        }
        query = query_from_form(fields, form)
        if len(query) == 0:
            return self.model.objects.select_related('morph').all()
        return self.model.objects.select_related('morph').filter(query)


######################
##==||  MORPHS  ||==##
######################


class MorphSearch(ListView):
    model = Morph
    template_name = 'gnosis/morph_search.html'
    
    def get_queryset(self):
        form = MorphForm(self.request.GET)
        fields = {
            'id': 'id',
            'name__icontains': 'name',
            'icon__icontains': 'icon',
            # 'for_folks': 'for_folks',
            # 'for_topics': 'for_topics',
            # 'for_creations': 'for_creations',
            # 'for_notes': 'for_notes',
        }
        query = query_from_form(fields, form)
        if len(query) == 0:
            return Morph.objects.all()
        return Morph.objects.filter(query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MorphForm(self.request.GET)
        return context


class MorphEdit(FormValidationMessagesMixin, UpdateView):
    model = Morph
    fields = ['name', 'json_data', 'icon']
    template_name = 'gnosis/morph_edit.html'
    # permission_required = 'gnosis.view_operation' #TODO include change permission to post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['json'] = self.object.json_data
        context['field_types'] = FIELD_TYPES #defined in models
        return context

    def get_success_url(self):
        return reverse('gnosis:morph_edit', kwargs={'pk':self.object.id})


class MorphCreate(FormValidationMessagesMixin, CreateView):
    model = Morph
    fields = ['name', 'json_data', 'icon'] 
    template_name = 'gnosis/morph_create.html'
    # permission_required = 'certification.add_commodity'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field_types'] = FIELD_TYPES #defined in models
        return context

    def get_success_url(self):
        return reverse('gnosis:morph_edit', kwargs={'pk':self.object.id})


#####################
##==||  FOLKS  ||==##
#####################


# class FolkSearch(SimpleSearchMixin, ListView):
#     model = Folk
#     template_name = 'gnosis/folk_search.html'
#     # permission_required = 'certification.view_operation'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = TopicForm(self.request.GET)
#         context['morphs'] = Morph.objects.filter(for_folks=True).order_by('name')
#         # messages.success(self.request, 'success')
#         # messages.error(self.request, 'error')
#         # messages.warning(self.request, 'warning')
#         # messages.info(self.request, 'info')
#         return context


# class FolkDetails(FormValidationMessagesMixin, MorphMatchMixin, DetailView):
#     model = Folk
#     template_name = 'gnosis/folk_details.html'

#     def get_queryset(self):
#         return Folk.objects.select_related('morph')

#     def get_success_url(self):
#         return reverse('gnosis:folk_details', kwargs={'pk':self.object.id})

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['morph_list'] = Morph.objects.filter(for_folks=True).order_by('name').all()
#         context['related_folks'] = [ record.child for record in FolkFolk.objects.filter(parent=self.object).select_related('child__morph') ]
#         context['related_folks'].extend([ record.parent for record in FolkFolk.objects.filter(child=self.object).select_related('parent__morph') ])
#         context['related_topics'] = [ record.topic for record in FolkTopic.objects.filter(folk=self.object).select_related('topic__morph') ]
#         context['related_notes'] = [ record.note for record in FolkNote.objects.filter(folk=self.object).select_related('note__morph') ]
#         return context


# class FolkEdit(FormValidationMessagesMixin, MorphMatchMixin, UpdateView):
#     model = Folk
#     fields = ['name', 'icon', 'json']
#     template_name = 'gnosis/folk_edit.html'

#     def get_queryset(self):
#         return Folk.objects.select_related('morph')

#     def get_success_url(self):
#         return reverse('gnosis:folk_details', kwargs={'pk':self.object.id})

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['morph_list'] = Morph.objects.filter(for_folks=True).order_by('name').all()
#         context['related_folks'] = [ record.child for record in FolkFolk.objects.filter(parent=self.object).select_related('child__morph') ]
#         context['related_folks'].extend([ record.parent for record in FolkFolk.objects.filter(child=self.object).select_related('parent__morph') ])
#         context['related_topics'] = [ record.topic for record in FolkTopic.objects.filter(folk=self.object).select_related('topic__morph') ]
#         context['related_notes'] = [ record.note for record in FolkNote.objects.filter(folk=self.object).select_related('note__morph') ]
#         return context


# class FolkCreate(FormValidationMessagesMixin, MorphMatchMixin, CreateView):
#     model = Folk
#     fields = ['morph', 'name', 'json']
#     template_name = 'gnosis/folk_create.html'

#     def get_success_url(self):
#         return reverse('gnosis:folk_details', kwargs={'pk':self.object.id})

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         morph = Morph.objects.get(id=self.kwargs['morph_id'])
#         context['selected_morph'] = morph
#         context['morph_list'] = Morph.objects.filter(for_folks=True).order_by('name').all()
#         return context


# ######################
# ##==||  TopicS  ||==##
# ######################


class TopicSearch(SimpleSearchMixin, ListView):
    model = Topic
    template_name = 'gnosis/topic_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TopicForm(self.request.GET)
        context['morphs'] = list(Morph.objects.order_by('name').values('id', 'name', 'icon'))
        context['results'] = list(self.object_list.values('id', 'name', 'icon', 'json_data', 'morph_id'))
        return context


class TopicDetails(FormValidationMessagesMixin, MorphMatchMixin, DetailView):
    model = Topic
    template_name = 'gnosis/topic_details.html'

    def get_queryset(self):
        return Topic.objects.select_related('morph')

    def get_success_url(self):
        return reverse('gnosis:topic_details', kwargs={'pk':self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['morph_list'] = Morph.objects.order_by('name').all()
        # context['related_topics'] = [ record.folk for record in .objects.filter(Topic=self.object).select_related('folk__morph') ]
        # context['related_notes'] = [ record.note for record in TopicNote.objects.filter(Topic=self.object).select_related('note__morph') ]
        return context


class TopicEdit(FormValidationMessagesMixin, MorphMatchMixin, UpdateView):
    model = Topic
    fields = ['name', 'icon', 'morph', 'json_data']
    template_name = 'gnosis/topic_edit.html'

    def get_queryset(self):
        return Topic.objects.select_related('morph')

    def get_success_url(self):
        return reverse('gnosis:topic_details', kwargs={'pk':self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['morph_list'] = Morph.objects.order_by('name').all()
        # context['related_folks'] = [ record.folk for record in FolkTopic.objects.filter(topic=self.object).select_related('folk__morph') ]
        # context['related_topics'] = [ record.child for record in TopicTopic.objects.filter(parent=self.object).select_related('child__morph') ]
        # context['related_topics'].extend([ record.parent for record in TopicTopic.objects.filter(child=self.object).select_related('parent__morph') ])
        # context['related_notes'] = [ record.note for record in TopicNote.objects.filter(topic=self.object).select_related('note__morph') ]
        return context


class TopicCreate(FormValidationMessagesMixin, MorphMatchMixin, CreateView):
    model = Topic
    fields = ['name', 'icon', 'morph', 'json_data']
    template_name = 'gnosis/topic_create.html'

    def get_success_url(self):
        return reverse('gnosis:topic_details', kwargs={'pk':self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_morph'] = Morph.objects.get(id=self.kwargs['morph_id'])
        context['morph_list'] = Morph.objects.order_by('name').all()
        return context


# #####################
# ##==||  NOTES  ||==##
# #####################


# class NoteSearch(SimpleSearchMixin, ListView):
#     model = Note
#     template_name = 'gnosis/note_search.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = TopicForm(self.request.GET)
#         context['morphs'] = Morph.objects.filter(for_notes=True).order_by('name')
#         return context


# class NoteDetails(FormValidationMessagesMixin, MorphMatchMixin, DetailView):
#     model = Note
#     template_name = 'gnosis/note_details.html'

#     def get_queryset(self):
#         return Note.objects.select_related('morph')

#     def get_success_url(self):
#         return reverse('gnosis:note_details', kwargs={'pk':self.object.id})

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['morph_list'] = Morph.objects.filter(for_notes=True).order_by('name').all()
#         context['related_folks'] = [ record.folk for record in FolkNote.objects.filter(note=self.object).select_related('folk__morph') ]
#         context['related_topics'] = [ record.topic for record in TopicNote.objects.filter(note=self.object).select_related('topic__morph') ]
#         context['related_notes'] = [ record.child for record in NoteNote.objects.filter(parent=self.object).select_related('child__morph') ]
#         context['related_notes'].extend([ record.parent for record in NoteNote.objects.filter(child=self.object).select_related('parent__morph') ])
#         return context


# class NoteEdit(FormValidationMessagesMixin, MorphMatchMixin, UpdateView):
#     model = Note
#     fields = ['name', 'icon', 'json', 'morph']
#     template_name = 'gnosis/note_edit.html'

#     def get_queryset(self):
#         return Note.objects.select_related('morph')

#     def get_success_url(self):
#         return reverse('gnosis:note_details', kwargs={'pk':self.object.id})

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['morph_list'] = Morph.objects.filter(for_notes=True).order_by('name').all()
#         context['related_folks'] = [ record.folk for record in FolkNote.objects.filter(note=self.object).select_related('folk__morph') ]
#         context['related_topics'] = [ record.topic for record in TopicNote.objects.filter(note=self.object).select_related('topic__morph') ]
#         context['related_notes'] = [ record.child for record in NoteNote.objects.filter(parent=self.object).select_related('child__morph') ]
#         context['related_notes'].extend([ record.parent for record in NoteNote.objects.filter(child=self.object).select_related('parent__morph') ])
#         return context


# class NoteCreate(FormValidationMessagesMixin, MorphMatchMixin, CreateView):
#     model = Note
#     fields = ['morph', 'name', 'json']
#     template_name = 'gnosis/note_create.html'

#     def get_success_url(self):
#         return reverse('gnosis:note_details', kwargs={'pk':self.object.id})

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['selected_morph'] = Morph.objects.get(id=self.kwargs['morph_id'])
#         context['morph_list'] = Morph.objects.filter(for_notes=True).order_by('name').all()
#         return context


# ####################
# ##==||  AJAX  ||==##
# ####################


# @login_required
# def catalog(request):
#     context = {}
#     if request.method != 'GET':
#         context['message'] = 'Endpoint accepts GET calls only'
#         return JsonResponse(context, status=400)
#     elif 'name' not in request.GET \
#     or 'topic' not in request.GET \
#     or request.GET['topic'] not in ['folk', 'topic', 'note']:
#         context['message'] = 'Must supply proper keys'
#         return JsonResponse(context, status=400)

#     if request.GET['topic'] == 'folk':
#         records = Folk.objects.filter(name__icontains=request.GET['name']).select_related('morph')
#     elif request.GET['topic'] == 'topic':
#         records = Topic.objects.filter(name__icontains=request.GET['name']).select_related('morph')
#     else:
#         records = Note.objects.filter(name__icontains=request.GET['name']).select_related('morph')
    
#     context['catalog'] = [{
#         'id': r.id,
#         'name': r.name,
#         'icon': r.icon if r.icon else r.morph.icon,
#     } for r in records]
#     return JsonResponse(context)


# @login_required
# @csrf_exempt
# def relate2(request):
#     context = {}
#     if request.method != 'POST':
#         context['message'] = 'Endpoint accepts POST calls only'
#         return JsonResponse(context, status=400)
    
#     elif 'topic_id' not in request.POST \
#     or 'topic' not in request.POST \
#     or 'related_id' not in request.POST \
#     or 'related' not in request.POST \
#     or request.POST['topic'] not in ['folk', 'topic', 'note'] \
#     or request.POST['related'] not in ['folk', 'topic', 'note']:
#         context['message'] = 'Must supply proper keys'
#         return JsonResponse(context, status=400)

    
#     model_dict = {
#         'folk': Folk,
#         'topic': Topic,
#         'note': Note,
#     }

#     model = model_dict[request.POST['topic']]
#     related_model = model_dict[request.POST['related']]

#     topic = model.objects.filter(id=request.POST['topic_id'])
#     related = related_model.objects.filter(id=request.POST['related_id']).select_related('morph')

#     if topic.count() == 0 or related.count() == 0:
#         context['message'] = 'Record(s) not found'
#         return JsonResponse(context, status=400)

#     topic = topic[0]
#     related = related[0]

#     if model == Folk:
#         if related_model == Folk:
#             new_record = FolkFolk.objects.create(parent=topic, child=related, json={})
#         elif related_model == Topic:
#             new_record = FolkTopic.objects.create(folk=topic, topic=related, json={})
#         else:
#             new_record = FolkNote.objects.create(folk=topic, note=related, json={})
#     elif model == Topic:
#         if related_model == Folk:
#             new_record = FolkTopic.objects.create(topic=topic, folk=related, json={})
#         elif related_model == Topic:
#             new_record = TopicTopic.objects.create(parent=topic, child=related, json={})
#         else:
#             new_record = TopicNote.objects.create(topic=topic, note=related, json={})
#     elif model == Note:
#         if related_model == Folk:
#             new_record = FolkNote.objects.create(note=topic, folk=related, json={})
#         elif related_model == Topic:
#             new_record = TopicNote.objects.create(note=topic, topic=related, json={})
#         else:
#             new_record = NoteNote.objects.create(parent=topic, child=related, json={})

#     context['message'] = 'Created'
#     return JsonResponse(context)


# @login_required
# @csrf_exempt
# def unrelate2(request):
#     context = {}
#     if request.method != 'POST':
#         context['message'] = 'Endpoint accepts POST calls only'
#         return JsonResponse(context, status=400)
    
#     elif 'topic_id' not in request.POST \
#     or 'topic' not in request.POST \
#     or 'related_id' not in request.POST \
#     or 'related' not in request.POST \
#     or request.POST['topic'] not in ['folk', 'topic', 'note'] \
#     or request.POST['related'] not in ['folk', 'topic', 'note']:
#         context['message'] = 'Must supply proper keys'
#         return JsonResponse(context, status=400)
    
#     # if request.POST['topic'] == 'folk':
#     #     model = Folk
#     # elif request.POST['topic'] == 'topic':
#     #     model = Topic
#     # else:
#     #     model = Note

#     # if request.POST['related'] == 'folk':
#     #     related_model = Folk
#     # elif request.POST['related'] == 'topic':
#     #     related_model = Topic
#     # else:
#     #     related_model = Note


#     model_dict = {
#         'folk': Folk,
#         'topic': Topic,
#         'note': Note,
#     }

#     model = model_dict[request.POST['topic']]
#     related_model = model_dict[request.POST['related']]

#     topic = model.objects.filter(id=request.POST['topic_id'])
#     related = related_model.objects.filter(id=request.POST['related_id'])

#     if topic.count() == 0 or related.count() == 0:
#         context['message'] = 'Record(s) not found'
#         return JsonResponse(context, status=400)

#     topic = topic[0]
#     related = related[0]

#     queryset = []
#     if model == Folk:
#         if related_model == Folk:
#             queryset = FolkFolk.objects.filter(parent=topic, child=related)
#             if queryset.count() == 0:
#                 queryset = FolkFolk.objects.filter(child=topic, parent=related)
#         elif related_model == Topic:
#             queryset = FolkTopic.objects.filter(folk=topic, topic=related)
#         else:
#             queryset = FolkNote.objects.filter(folk=topic, note=related)
#     elif model == Topic:
#         if related_model == Folk:
#             queryset = FolkTopic.objects.filter(topic=topic, folk=related)
#         elif related_model == Topic:
#             queryset = TopicTopic.objects.filter(parent=topic, child=related)
#             if queryset.count() == 0:
#                 queryset = TopicTopic.objects.filter(child=topic, parent=related)
#         else:
#             queryset = TopicNote.objects.filter(topic=topic, note=related)
#     elif model == Note:
#         if related_model == Folk:
#             queryset = FolkNote.objects.filter(note=topic, folk=related)
#         elif related_model == Topic:
#             queryset = TopicNote.objects.filter(note=topic, topic=related)
#         else:
#             queryset = NoteNote.objects.filter(parent=topic, child=related)
#             if queryset.count() == 0:
#                 queryset = NoteNote.objects.filter(child=topic, parent=related)

#     if len(queryset) == 0:
#         context['message'] = 'Record not found'
#         return JsonResponse(context, status=400)
    
#     queryset[0].delete()
#     context['message'] = 'Record deleted'
#     return JsonResponse(context)


# @login_required
# @csrf_exempt
# def relate(request):
#     context = {}
#     if request.method != 'POST':
#         context['message'] = 'Endpoint accepts POST calls only'
#         return JsonResponse(context, status=400)
    
#     elif 'topic_id' not in request.POST \
#     or 'related_id' not in request.POST:
#         context['message'] = 'Must supply proper ids'
#         return JsonResponse(context, status=400)

    
#     model_dict = {
#         'folk': Folk,
#         'topic': Topic,
#         'note': Note,
#     }
#     model = model_dict[request.POST['topic']]
#     related_model = model_dict[request.POST['related']]

#     topic = model.objects.filter(id=request.POST['topic_id'])
#     related = related_model.objects.filter(id=request.POST['related_id']).select_related('morph')

#     if topic.count() == 0 or related.count() == 0:
#         context['message'] = 'Record(s) not found'
#         return JsonResponse(context, status=400)

#     topic = topic[0]
#     related = related[0]

#     if model == Folk:
#         if related_model == Folk:
#             new_record = FolkFolk.objects.create(parent=topic, child=related, json={})
#         elif related_model == Topic:
#             new_record = FolkTopic.objects.create(folk=topic, topic=related, json={})
#         else:
#             new_record = FolkNote.objects.create(folk=topic, note=related, json={})
#     elif model == Topic:
#         if related_model == Folk:
#             new_record = FolkTopic.objects.create(topic=topic, folk=related, json={})
#         elif related_model == Topic:
#             new_record = TopicTopic.objects.create(parent=topic, child=related, json={})
#         else:
#             new_record = TopicNote.objects.create(topic=topic, note=related, json={})
#     elif model == Note:
#         if related_model == Folk:
#             new_record = FolkNote.objects.create(note=topic, folk=related, json={})
#         elif related_model == Topic:
#             new_record = TopicNote.objects.create(note=topic, topic=related, json={})
#         else:
#             new_record = NoteNote.objects.create(parent=topic, child=related, json={})

#     context['message'] = 'Created'
#     return JsonResponse(context)


# @login_required
# @csrf_exempt
# def unrelate(request):
#     context = {}
#     if request.method != 'POST':
#         context['message'] = 'Endpoint accepts POST calls only'
#         return JsonResponse(context, status=400)
    
#     elif 'topic_id' not in request.POST \
#     or 'topic' not in request.POST \
#     or 'related_id' not in request.POST \
#     or 'related' not in request.POST \
#     or request.POST['topic'] not in ['folk', 'topic', 'note'] \
#     or request.POST['related'] not in ['folk', 'topic', 'note']:
#         context['message'] = 'Must supply proper keys'
#         return JsonResponse(context, status=400)
    
#     # if request.POST['topic'] == 'folk':
#     #     model = Folk
#     # elif request.POST['topic'] == 'topic':
#     #     model = Topic
#     # else:
#     #     model = Note

#     # if request.POST['related'] == 'folk':
#     #     related_model = Folk
#     # elif request.POST['related'] == 'topic':
#     #     related_model = Topic
#     # else:
#     #     related_model = Note


#     model_dict = {
#         'folk': Folk,
#         'topic': Topic,
#         'note': Note,
#     }

#     model = model_dict[request.POST['topic']]
#     related_model = model_dict[request.POST['related']]

#     topic = model.objects.filter(id=request.POST['topic_id'])
#     related = related_model.objects.filter(id=request.POST['related_id'])

#     if topic.count() == 0 or related.count() == 0:
#         context['message'] = 'Record(s) not found'
#         return JsonResponse(context, status=400)

#     topic = topic[0]
#     related = related[0]

#     queryset = []
#     if model == Folk:
#         if related_model == Folk:
#             queryset = FolkFolk.objects.filter(parent=topic, child=related)
#             if queryset.count() == 0:
#                 queryset = FolkFolk.objects.filter(child=topic, parent=related)
#         elif related_model == Topic:
#             queryset = FolkTopic.objects.filter(folk=topic, topic=related)
#         else:
#             queryset = FolkNote.objects.filter(folk=topic, note=related)
#     elif model == Topic:
#         if related_model == Folk:
#             queryset = FolkTopic.objects.filter(topic=topic, folk=related)
#         elif related_model == Topic:
#             queryset = TopicTopic.objects.filter(parent=topic, child=related)
#             if queryset.count() == 0:
#                 queryset = TopicTopic.objects.filter(child=topic, parent=related)
#         else:
#             queryset = TopicNote.objects.filter(topic=topic, note=related)
#     elif model == Note:
#         if related_model == Folk:
#             queryset = FolkNote.objects.filter(note=topic, folk=related)
#         elif related_model == Topic:
#             queryset = TopicNote.objects.filter(note=topic, topic=related)
#         else:
#             queryset = NoteNote.objects.filter(parent=topic, child=related)
#             if queryset.count() == 0:
#                 queryset = NoteNote.objects.filter(child=topic, parent=related)

#     if len(queryset) == 0:
#         context['message'] = 'Record not found'
#         return JsonResponse(context, status=400)
    
#     queryset[0].delete()
#     context['message'] = 'Record deleted'
#     return JsonResponse(context)
