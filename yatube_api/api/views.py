from rest_framework import viewsets, filters
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsOwnerOrReadOnly
from posts.models import Post, Group
from api.serializers import (PostSerializer,
                             GroupSerializer,
                             CommentSerializer,
                             FollowSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления постами.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """
        Создание поста с указанием автора.
        """
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра групп.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsOwnerOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления комментариями.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_post(self):
        """
        Получение объекта поста по post_id.
        """
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        """
        Получение комментариев для поста.
        """
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        """
        Создание комментария с привязкой к посту.
        """
        post = self.get_post()
        serializer.save(author=self.request.user,
                        post=post)


class FollowViewSet(viewsets.ModelViewSet):
    """
    ViewSet для подписок.
    """
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']
    permission_classes = [IsAuthenticated,
                          IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Получение подписок только для уникального автора.
        """
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """
        Получение данных пользователя для автозаполнения.
        """
        serializer.save(user=self.request.user)
