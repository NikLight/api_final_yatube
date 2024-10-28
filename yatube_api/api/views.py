from rest_framework import viewsets, filters
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import (IsOwnerOrReadOnly,
                             NonAuthorizedUserIsNotAllowed)
from posts.models import Post, Group, Follow
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

    def get_permissions(self):
        """
        Проверка авторизации для POST запроса.
        """
        if self.action == 'create':
            return (NonAuthorizedUserIsNotAllowed(), )

        return super().get_permissions()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра групп.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_permissions(self):
        """
        Проверка авторизации для POST запроса.
        """
        if self.action == 'create':
            return (NonAuthorizedUserIsNotAllowed(),)

        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления комментариями.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_permissions(self):
        """
        Проверка авторизации для POST запроса.
        """
        if self.action == 'create':
            return (NonAuthorizedUserIsNotAllowed(),)

        return super().get_permissions()

    def get_queryset(self):
        """
        Получение комментариев для поста.
        """
        post_id = get_object_or_404(
            Post,
            id=self.kwargs.get('post_id'))

        return post_id.comments.all()

    def perform_create(self, serializer):
        """
        Создание комментария с привязкой к посту.
        """
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(post=post, author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    """
    ViewSet для подписок.
    """
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']
    permission_classes = [IsOwnerOrReadOnly]

    def get_permissions(self):
        """
        Проверка авторизации для POST запроса.
        """
        if self.action:
            return (NonAuthorizedUserIsNotAllowed(),)
        return super().get_permissions()

    def get_queryset(self):
        """
        Получение подписок только для уникального автора.
        """
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Получение данных slug пользователя, для автозаполнения.
        """
        serializer.save(user=self.request.user)
