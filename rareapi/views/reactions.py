from rareapi.models.posts import Post
from django.core.exceptions import ValidationError
from django.db import models
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Reaction, PostReaction, RareUser

class Reactions(ViewSet):
    def create(self, request):

        reaction = Reaction()
        reaction.label= request.data['label']
        reaction.image_url = request.data['image_url']

        try:
            reaction.save()
            serializer = ReactionSerializer(reaction, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        reactions = Reaction.objects.all()

        serializer = ReactionSerializer(reactions, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def react(self, request, pk=None):

        if request.method == "POST":
            reaction = Reaction.objects.get(pk=pk)
            post = Post.objects.get(pk=request.data['post'])
            rare_user = RareUser.objects.get(user=request.auth.user)
            try:
                post_react = PostReaction.objects.get(reaction=reaction, post=post, user=rare_user)
                return Response(
                    {'message': 'Already added this reaction'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except PostReaction.DoesNotExist: 
                post_react = PostReaction()
                post_react.user = rare_user
                post_react.reaction = reaction
                post_react.post = post
                post_react.save()

                return Response({}, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            reaction = Reaction.objects.get(pk=pk)
            post = Post.objects.get(pk=request.data['post'])
            rare_user = RareUser.objects.get(user=request.auth.user)
            try:
                reaction = Reaction.objects.get(pk=pk)
            except Reaction.DoesNotExist:
                return Response(
                    {'message': 'Reaction does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try: 
                post_react = PostReaction.objects.get(reaction=reaction, post=post, user = rare_user)
                post_react.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except PostReaction.DoesNotExist:
                return Response({'message': 'Reaction not currently set.'},
                status=status.HTTP_404_NOT_FOUND
                )


        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url',)