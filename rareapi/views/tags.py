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
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single Post
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ( 'id', 'label', )
        depth=1
