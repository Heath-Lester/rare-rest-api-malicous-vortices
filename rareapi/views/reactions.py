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


    # Custom action that toggles a post_reaction into/out of being by checking if the post matches criteria sent by client and acting accordingly

    @action(methods=['post'], detail=True)
    def react(self, request, pk=None):

        if request.method == "POST":
            reaction = Reaction.objects.get(pk=pk)
            post = Post.objects.get(pk=request.data['post'])
            rare_user = RareUser.objects.get(user=request.auth.user)
            try:
                post_react = PostReaction.objects.get(reaction=reaction, post=post, user=rare_user)
                post_react.delete()
                return Response(
                    {'message': 'Delete successful'},
                    status=status.HTTP_204_NO_CONTENT
                )
            except PostReaction.DoesNotExist: 
                post_react = PostReaction()
                post_react.user = rare_user
                post_react.reaction = reaction
                post_react.post = post
                post_react.save()

                return Response({}, status=status.HTTP_201_CREATED)

class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url',)