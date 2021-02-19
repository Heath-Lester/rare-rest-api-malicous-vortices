from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Tag

class Tags(ViewSet):
    
    def create(self, request):
        tag = Tag()

        tag.label = request.data['label']

        try:
            tag.save()
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        tags = Tag.objects.all()

        serializer = TagSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):

        tag = Tag.objects.get(pk=pk)
        tag.label = request.data['label']

        tag.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ( 'id', 'label', )
