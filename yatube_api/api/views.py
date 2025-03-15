from rest_framework import viewsets, generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from api.serializers import (PostSerializer,
                             GroupSerializer,
                             CommentSerializer)
from posts.models import Post, Group, Comment


class PostViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = generics.get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def create(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied(
                "Необходима аутентификация для создания поста!")
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        if not request.user.is_authenticated:
            raise PermissionDenied(
                "Необходима аутентификация для редактирования поста!")
        queryset = Post.objects.all()
        post = generics.get_object_or_404(queryset, pk=pk)
        if post.author != request.user:
            raise PermissionDenied("Нельзя редактировать чужой пост!")
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        if not request.user.is_authenticated:
            raise PermissionDenied(
                "Необходима аутентификация для редактирования поста!")
        queryset = Post.objects.all()
        post = generics.get_object_or_404(queryset, pk=pk)
        if post.author != request.user:
            raise PermissionDenied("Нельзя редактировать чужой пост!")
        serializer = PostSerializer(post,
                                    data=request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        if not request.user.is_authenticated:
            raise PermissionDenied(
                "Необходима аутентификация для удаления поста!")
        queryset = Post.objects.all()
        post = generics.get_object_or_404(queryset, pk=pk)
        if post.author != request.user:
            raise PermissionDenied(
                "Нельзя удалить пост другого пользователя!")
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Group.objects.all()
        group = generics.get_object_or_404(queryset, pk=pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentViewSet(viewsets.ViewSet):
    def list(self, request, post_id=None):
        queryset = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, post_id=None):
        queryset = Comment.objects.filter(post_id=post_id)
        comment = generics.get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def create(self, request, post_id=None):
        if not request.user.is_authenticated:
            raise PermissionDenied(
                "Необходима аутентификация для добавления комментария!")
        post = generics.get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, post_id=None):
        if not request.user.is_authenticated:
            raise PermissionDenied(
                "Необходима аутентификация для редактирования комментария!")
        queryset = Comment.objects.filter(post_id=post_id)
        comment = generics.get_object_or_404(queryset, pk=pk)
        if comment.author != request.user:
            raise PermissionDenied("Нельзя редактировать чужой комментарий!")
        serializer = CommentSerializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None, post_id=None):
        if not request.user.is_authenticated:
            raise PermissionDenied(
                "Необходима аутентификация для редактирования комментария!")
        queryset = Comment.objects.filter(post_id=post_id)
        comment = generics.get_object_or_404(queryset, pk=pk)
        if comment.author != request.user:
            raise PermissionDenied(
                "Нельзя редактировать чужой комментарий!")
        serializer = CommentSerializer(comment,
                                       data=request.data,
                                       partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, post_id=None):
        if not request.user.is_authenticated:
            raise PermissionDenied(
                "Необходима аутентификация для удаления комментария!")
        queryset = Comment.objects.filter(post_id=post_id)
        comment = generics.get_object_or_404(queryset, pk=pk)
        if comment.author != request.user:
            raise PermissionDenied(
                "Нельзя удалить комментарий другого пользователя!")
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
