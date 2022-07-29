from rest_framework import serializers
from games.models import Game, GameCategory, Player, PlayerScore

# class GameSerializer(serializers.Serializer):
#     pk = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=200)
#     release_date = serializers.DateTimeField("")
#     game_category = serializers.CharField(max_length=200)
#     played = serializers.BooleanField(required=False)

#     def create(self, validated_data):
#         return Game.objects.create(**validated_data)

#     def update(self, instance: Game, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.release_date = validated_data.get(
#             'release_date', instance.release_date)
#         instance.game_category = validated_data.get(
#             'game_category', instance.game_category)
#         instance.played = validated_data.get('played', instance.played)
#         instance.save()
#         return instance


class GameSerializer(serializers.HyperlinkedModelSerializer):
    game_category = serializers.SlugRelatedField(
        slug_field="name",
        queryset=GameCategory.objects.all()
    )

    class Meta:
        model = Game
        fields = (
            'url',
            'name',
            'release_date',
            'game_category',
            'played'
        )


class GameCategorySerializer(serializers.HyperlinkedModelSerializer):
    games = serializers.HyperlinkedRelatedField(
        view_name='gamecategory-detail',
        many=True,
        read_only=True,
    )

    class Meta:
        model = GameCategory
        fields = (
            'url',
            'pk',
            'name',
            'games'
        )


class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    game = GameSerializer()

    class Meta:
        model = PlayerScore
        fields = (
            'url',
            'pk',
            'score',
            'score_date',
            'game',
        )


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    scores = ScoreSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(
        choices=Player.GENDER_CHOICES
    )
    gender_description = serializers.CharField(
        source='get_gender_display',
        read_only=True
    )

    class Meta:
        model = Player
        fields = (
            'url',
            'name',
            'gender',
            'gender_description',
            'scores',
        )


class PlayerScoreSerializer(serializers.HyperlinkedModelSerializer):
    player = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Player.objects.all()
    )
    game = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Game.objects.all()
    )

    class Meta:
        model = PlayerScore
        fields = (
            'url',
            'pk',
            'score',
            'score_date',
            'player',
            'game',
        )
