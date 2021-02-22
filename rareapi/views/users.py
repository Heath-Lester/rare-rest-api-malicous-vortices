from rareapi.models.subscriptions import Subscription
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
from datetime import datetime
from django.contrib.auth.models import User


class Users(ViewSet):
    """Users"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single User
        Returns:
            Response -- JSON serialized User instance
        """
        

        rare_user = RareUser.objects.get(pk=pk)

        serializer = RareUserSerializer(rare_user, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a User
        Returns:
            Response -- Empty body with 204 status code
        """
    
    def patch(self, request, pk=None):
        """Handle PATCH requests for a User
        Returns:
            Response -- Empty body with 204 status code
        """
        user = RareUser.objects.get(pk=pk)
        user.active = request.data['active']
        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

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

    @action(methods=['post'], detail=True)
    def subscribe(self, request, pk=None):

        if request.method == "POST":
            author = RareUser.objects.get(pk=pk)
            follower = RareUser.objects.get(user=request.auth.user)
            if author == follower:
                return Response({'message': 'User cannot subscribe to themselves'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                subscription = Subscription.objects.get(author=author, follower=follower)
                if subscription.ended_on:
                    subscription.created_on = datetime.now()
                    subscription.ended_on = None
                    subscription.save()
                    return Response({'message' : 'Subscription Renewed'}, status=status.HTTP_204_NO_CONTENT)
                else:
                    subscription.ended_on = datetime.now()
                    subscription.save()
                    return Response({'message' : 'Subscription Ended'}, status=status.HTTP_204_NO_CONTENT)
            except Subscription.DoesNotExist: 
                subscription = Subscription()
                subscription.author = author
                subscription.follower = follower
                subscription.created_on = datetime.now()
                subscription.save()

                return Response({}, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def admin(self, request, pk=None):
        
        if request.method == "POST":
            if request.auth.user.is_staff:
                rare_user_target = RareUser.objects.get(pk=pk)
                if rare_user_target.user.is_staff:
                    target_user=rare_user_target.user
                    target_user.is_staff = False
                    target_user.save()
                    return Response({'message' : 'Admin rights revoked'}, status=status.HTTP_204_NO_CONTENT)
                else:
                    target_user=rare_user_target.user
                    target_user.is_staff = True
                    target_user.save()
                    return Response({'message' : 'New admin approved'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message' : 'Non-admins may not change user privileges'}, status=status.HTTP_401_UNAUTHORIZED)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for Users
    Arguments:
        serializer type
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_staff')

class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('author', 'created_on', 'ended_on')
        depth = 1


class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for RareUsers
    Arguments:
        serializer type
    """
    user = UserSerializer(many=False)
    subscriptions = SubscriptionSerializer(many=True)

    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'active', 'subscriptions')
        depth = 1
