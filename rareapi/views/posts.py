"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
<<<<<<< HEAD
from rareapi.models import Post, RareUser, Category, Tag, PostTag
from rest_framework.decorators import action
=======
from rareapi.models import Post, RareUser, Category, PostReaction, Reaction
from datetime import date

>>>>>>> main

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
        post.publication_date = date.today()
        post.image_url = request.data["imageUrl"]
        post.content = request.data["content"]
        
        if user.user.is_staff:
            post.approved = True
        else:
            post.approved = False

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
            associated_tags=Tag.objects.filter(related_post__post=post)
            print(associated_tags)

            all_tags=serializer=TagSerializer(associated_tags, many=True, context={'request',request})
            my_post=serializer = PostSerializer(post, context={'request': request})
            
            single_post={}
            single_post['post']=my_post.data
            single_post['tags']=all_tags.data
            # post['all_tags']=all_tags.data
            print(single_post)
            return Response(single_post)
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

        title = self.request.query_params.get('title', None)
        if title is not None:
            posts = posts.filter(title__contains=title)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)


    @action(methods=[ 'post', 'delete'], detail=True)
    def addtag(self, request, pk=None):

        if request.method=="POST":
            
            post=Post.objects.get(pk=pk)
            tag=Tag.objects.get(pk=request.data["tag_id"])
            try:
                post_tag = PostTag.objects.get(post=post, tag=tag)
                return Response(
                    {'message': 'this tag is on the post.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            except PostTag.DoesNotExist:    
                post_tag=PostTag()
                post_tag.post=post
                post_tag.tag=tag
                post_tag.save()
                return Response({}, status=status.HTTP_201_CREATED)

        elif request.method=="DELETE":
            try:
                post=Post.objects.get(pk=pk)

            except Post.DoesNotExist:
                return Response(
                    {'message': 'Post does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # user = RareUser.objects.get(user=request.auth.user)
            try:
                post=Post.objects.get(pk=pk)
                
                tag=Tag.objects.get(pk=request.data["tag_id"])
                
                post_tag = PostTag.objects.get(post=post, tag=tag)
                
                post_tag.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except PostTag.DoesNotExist:
                return Response(
                    {'message': 'tag is not on the post'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ( 'id', 'label' )

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date',
                  'image_url', 'content', 'approved',"related_post" )
        depth = 1
