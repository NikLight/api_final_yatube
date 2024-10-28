from django.urls import path, include
from rest_framework import routers

from api.views import (PostViewSet,
                       GroupViewSet,
                       CommentViewSet,
                       FollowViewSet)

# Создаем маршрутизатор для управления URL
api_router_v1 = routers.DefaultRouter()

# Регистрируем эндпоинт для постов
api_router_v1.register(r'posts',
                       PostViewSet,
                       basename='posts')

# Регистрируем эндпоинт для групп
api_router_v1.register(r'groups',
                       GroupViewSet,
                       basename='groups')

# Регистрируем эндпоинт для комментариев
api_router_v1.register(r'posts/(?P<post_id>\d+)/comments',
                       CommentViewSet,
                       basename='comments')

# Регистрируем эндпоинт для подписок
api_router_v1.register(r'follow',
                       FollowViewSet,
                       basename='follow')

# Основные маршруты приложения
urlpatterns = [
    # Включаем маршруты, сгенерированные роутером
    path('v1/', include(api_router_v1.urls)),

    #настроили JWS
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
