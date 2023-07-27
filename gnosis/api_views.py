# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework import viewsets, generics
from .serializers import *
from .models import *


class ListCreateMorphs(generics.ListCreateAPIView): #viewsets.ModelViewSet
    queryset = Morph.objects.all()
    serializer_class = MorphSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class UpdateMorph(generics.UpdateAPIView): #viewsets.ModelViewSet
    queryset = Morph.objects.all()
    serializer_class = MorphSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ListTopics(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    # permission_classes = [permissions.IsAuthenticated]



def upsert_morph(request):
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