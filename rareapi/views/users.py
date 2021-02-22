from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post, RareUser, Category, PostReaction, Reaction
from datetime import date
from django.contrib.auth.models import User


class Users(ViewSet):
    """Users"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single User
        Returns:
            Response -- JSON serialized User instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/Users/2
            #
            # The `2` at the end of the route becomes `pk`
            post = Post.objects.get(pk=pk)
            associated_tags = Tag.objects.filter(related_post__post=post)
            print(associated_tags)

            all_tags = serializer = TagSerializer(
                associated_tags, many=True, context={'request', request})
            my_post = serializer = PostSerializer(
                post, context={'request': request})

            single_post = {}
            single_post['post'] = my_post.data
            single_post['tags'] = all_tags.data
            # post['all_tags']=all_tags.data
            print(single_post)
            return Response(single_post)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a User
        Returns:
            Response -- Empty body with 204 status code
        """

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single User
        Returns:
            Response -- 200, 404, or 500 status code
        """

    def list(self, request):
        """Handle GET requests to /users resource
        Returns:
            Response -- JSON serialized list of Users
        """
        # Get all Post records from the database
        rare_user = RareUser.objects.get(user=request.auth.user)

        if rare_user.user.is_staff:
            rare_users = RareUser.objects.all()

            serializer = RareUserSerializer(
                rare_users, many=True, context={'request': request})
            return Response(serializer.data)

        else:
            return Response({'message': "This User does not have admin privileges."}, status=status.HTTP_401_UNAUTHORIZED)
            # Support filtering Users by type
            #    http://localhost:8000/Users?type=1
            #
            # That URL will retrieve all tabletop Users


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for Users
    Arguments:
        serializer type
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_staff', 'username')


class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for RareUsers
    Arguments:
        serializer type
    """
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'active')
        depth = 1
