from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from django.contrib.auth.models import User

from posts.models import Comment, Post, Group, Follow


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели поста.
    Включает связанные комментарии.
    """
    comments = serializers.StringRelatedField(
        many=True, required=False)
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False)

    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели группы.
    """

    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'slug',
            'description',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'text',
            'created',
            'post'
        )
        read_only_fields = ('author', 'post')


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подписок.
    Включает проверку уникальности.
    """
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Follow
        fields = ('user', 'following',)

    def create(self, validated_data):
        following = validated_data.pop('following')
        user = self.context['request'].user

        if user == following:
            raise ValidationError(
                'Вы не можете подписаться на самого себя')

        if Follow.objects.filter(
                user=user,following=following).exists():
            raise ValidationError(
                'Вы уже подписаны на этого пользователя')

        follower = Follow.objects.create(
            user=user,
            following=following)

        return follower
