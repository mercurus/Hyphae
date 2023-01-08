from django.core.cache import cache
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django import forms
from .models import *


class MorphForm(forms.ModelForm):
    id = forms.IntegerField(label='ID', required=False)
    class Meta:
        model = Morph
        fields = '__all__'


# class TopicForm(forms.Form):
#     id = forms.IntegerField(label='ID', required=False)
#     name = forms.CharField(label='Name', required=False)
#     json_data = forms.CharField(label='Json', required=False)
#     icon = forms.CharField(label='Icon', required=False)
#     morph = forms.IntegerField(label='Morph ID', required=False)


# class FolkForm(forms.ModelForm):
#     id = forms.IntegerField(label='ID', required=False)
#     class Meta:
#         model = Folk
#         fields = ['name', 'json', 'icon', 'morph']


class TopicForm(forms.ModelForm):
    id = forms.IntegerField(label='ID', required=False)
    class Meta:
        model = Topic
        fields = ['name', 'json_data', 'icon', 'morph']


# # class CreationForm(forms.ModelForm):
# #     id = forms.IntegerField(label='ID', required=False)
# #     class Meta:
# #         model = Creation
# #         fields = ['name', 'json', 'morph']


# class NoteForm(forms.ModelForm):
#     id = forms.IntegerField(label='ID', required=False)
#     class Meta:
#         model = Note
#         fields = ['name', 'json', 'icon', 'morph']




        # widgets = {
        #     'preamble': forms.Textarea(attrs={'cols':50, 'rows':3, 'maxlength':3000}),
        # }



# MorphForm = forms.modelform_factory(Morph,  fields=['id', 'name', 'json_template', 'for_folks', 'for_topics', 'for_creations', 'for_notes'])


# class BaseQuestionFormSet(forms.BaseFormSet):
#   """Used when creating Inquiries"""
#   def clean(self):
#       if any(self.errors):
#           return

#       for form in self.forms:
#           if form.cleaned_data:
#               pass
#           pass


#QuestionFormset = formset_factory(Question, formset=BaseQuestionFormSet, extra=1)
# ChoiceFormSet = inlineformset_factory(Question, Choice, exclude=('note',), can_delete=False, extra=1)


# class BaseQuestionFormSet(BaseInlineFormSet):
#   """https://micropyramid.com/blog/how-to-use-nested-formsets-in-django/"""
#   def __init__(self, *args, **kwargs):
#       super().__init__(*args, **kwargs)
#       #self.queryset = Question.objects.filter(name__startswith='O')
#   def add_fields(self, form, index):
#       super(BaseQuestionFormSet, self).add_fields(form, index)
#       # save the formset in the 'nested' property
#       form.nested = ChoiceFormset(
#           instance=form.instance,
#           data=form.data if form.is_bound else None,
#           files=form.files if form.is_bound else None,
#           prefix='choice-{}-{}'.format(form.prefix, ChoiceFormset.get_default_prefix()),
#           extra=1)
#   def is_valid(self):
#       result = super(BaseQuestionFormSet, self).is_valid()
#       if self.is_bound:
#           for form in self.forms:
#               if hasattr(form, 'nested'):
#                   result = result and form.nested.is_valid()
#       return result
#   def save(self, commit=True):
#       result = super(BaseQuestionFormSet, self).save(commit=commit)
#       for form in self.forms:
#           if hasattr(form, 'nested'):
#               if not self._should_delete_form(form):
#                   form.nested.save(commit=commit)
#       return result
