"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post, RareUser, Category, PostReaction, Reaction


class Posts(ViewSet):
    """Posts"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Post instance
        """

        # Uses the token passed in the `Authorization` header
        user = RareUser.objects.get(user=request.auth.user)

        # Create a new Python instance of the Post class
        # and set its properties from what was sent in the
        # body of the request from the client.
        post = Post()
        post.user = user
        post.title = request.data["title"]
        post.publication_date = request.data["publicationDate"]
        post.image_url = request.data["imageUrl"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `categoryId` in the body of the request.
        category = Category.objects.get(pk=request.data["categoryId"])
        post.category = category

        # Try to save the new Post to the database, then
        # serialize the Post instance as JSON, and send the
        # JSON as a response to the client request
        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Post
        Returns:
            Response -- JSON serialized Post instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/Posts/2
            #
            # The `2` at the end of the route becomes `pk`
            post = Post.objects.get(pk=pk)
            # Gets all reactions and initializes an empty array
            reactions = Reaction.objects.all()
            post.reaction_count=[]


            # Loops over queryset of all reactions, and for each one counts how PostReactions exist that correspond both to that post and that reaction.
            # Then appends the result of that to the reaction_count list as a dictionary with key=reaction.label and value = number_of_reactions 
            for reaction in reactions:
                number_of_reactions = PostReaction.objects.filter(post=post, reaction=reaction).count()
                post.reaction_count.append({reaction.label: number_of_reactions})

            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a Post
        Returns:
            Response -- Empty body with 204 status code
        """
        user = RareUser.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Post, get the Post record
        # from the database whose primary key is `pk`
        post = Post.objects.get(pk=pk)
        post.user = user
        post.title = request.data["title"]
        post.publication_date = request.data["publicationDate"]
        post.image_url = request.data["imageUrl"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `categoryId` in the body of the request.
        category = Category.objects.get(pk=request.data["categoryId"])
        post.category = category

        post.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single Post
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to Posts resource
        Returns:
            Response -- JSON serialized list of Posts
        """
        # Get all Post records from the database
        posts = Post.objects.all()

        # Support filtering Posts by type
        #    http://localhost:8000/Posts?type=1
        #
        # That URL will retrieve all tabletop Posts
        category = self.request.query_params.get('category', None)
        if category is not None:
            posts = posts.filter(category__id=category)
            
        user = RareUser.objects.get(user=request.auth.user)
        active = self.request.query_params.get('active', None)

        if active is not None:
            posts = posts.filter(user__id=user.id)

        user = self.request.query_params.get('user', None)
        if user is not None:
            posts = posts.filter(user__id=user)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for Posts
    Arguments:
        serializer type
    """
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date',
                  'image_url', 'content', 'approved', 'reaction_count')
        depth = 2
