from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.throttling import ScopedRateThrottle

from games.models import Game, GameCategory, Player, PlayerScore
from games.permissions import IsOwnerOrReadOnly
from games.serializers import PlayerScoreSerializer, PlayerSerializer, UserSerializer
from games.serializers import GameCategorySerializer, GameSerializer


class GameCategoryList(generics.ListCreateAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = "gamecategory-list"
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = "game-categories"


class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = "gamecategory-detail"
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = "game-categories"


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = "game-list"
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = "game-detail"
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = "player-list"


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = "player-detail"


class PlayerScoreList(generics.ListCreateAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = "playerscore-list"


class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = "playerscore-detail"


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = "user-list"


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = "user-detail"


class ApiRoot(generics.ListAPIView):
    name = "api-root"

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "players": request.build_absolute_uri(reverse(PlayerList.name)),
                "game-categories": request.build_absolute_uri(
                    reverse(GameCategoryList.name)
                ),
                "games": request.build_absolute_uri(reverse(GameList.name)),
                "scores": request.build_absolute_uri(reverse(PlayerScoreList.name)),
                "users": request.build_absolute_uri(reverse(UserList.name)),
            }
        )
