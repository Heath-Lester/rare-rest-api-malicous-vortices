from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Comment, RareUser, Post
from datetime import date

class Comments(ViewSet):
    def list(self, request):
        comments=Comment.objects.all()
        serializer = CommentSerializer(comments, many=True, context= {'request': request})
        return Response(serializer.data)
    
    def create(self, request):
       
        author= RareUser.objects.get(user=request.auth.user)
        post=Post.objects.get(pk=request.data["postId"])


        comment=Comment()
        comment.post=post
        comment.author=author
        comment.content=request.data["content"]
        comment.created_on= date.today()

        try:
            comment.save()
            serializer=CommentSerializer(comment, context= {'request': request} )
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        comment = Comment.objects.get(pk=pk)
        comment.content = request.data['content']
        comment.created_on = date.today()

        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):

        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=('id','post', 'author', 'content', 'created_on')
        depth=2
