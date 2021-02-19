from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Category


class Categories(ViewSet):

    def create(self, request):
        category = Category()

        category.label = request.data['label']

        try:
            category.save()
            serializer = CategorySerializer(
                category, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        categories = Category.objects.all()

        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):

        category = Category.objects.get(pk=pk)
        category.label = request.data['label']

        category.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'label', )
