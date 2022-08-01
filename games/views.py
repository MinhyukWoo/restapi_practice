from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.throttling import ScopedRateThrottle
from django_filters import rest_framework as filters
from django_filters import NumberFilter, DateTimeFilter, AllValuesFilter

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
    filterset_fields = ("name",)
    search_fields = ("^name",)
    ordering_fields = ("name",)


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
    filterset_fields = (
        "name",
        "game_category",
        "release_date",
        "played",
        "owner",
    )
    search_fields = ("^name",)
    ordering_fields = (
        "name",
        "release_date",
    )

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
    filterset_fields = ("name",)
    search_fields = ("^name",)
    ordering_fields = ("name",)


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = "player-detail"


class PlayerScoreFilter(filters.FilterSet):
    min_score = NumberFilter(field_name="score", lookup_expr="gte")
    max_score = NumberFilter(field_name="score", lookup_expr="lte")
    from_score_date = DateTimeFilter(field_name="score_date", lookup_expr="gte")
    to_score_date = DateTimeFilter(field_name="score_date", lookup_expr="lte")
    player_name = AllValuesFilter(field_name="player__name")
    game_name = AllValuesFilter(field_name="game__name")

    class Meta:
        model = PlayerScore
        fields = (
            "score",
            "from_score_date",
            "to_score_date",
            "min_score",
            "max_score",
            "player_name",
            "game_name",
        )


class PlayerScoreList(generics.ListCreateAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = "playerscore-list"
    filterset_class = PlayerScoreFilter
    ordering_fields = (
        "score",
        "score_date",
    )


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
