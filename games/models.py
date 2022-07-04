from django.db import models


class GameCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Game(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, unique=True)
    release_date = models.DateTimeField()
    game_category = models.ForeignKey(
        GameCategory,
        on_delete=models.CASCADE,
        related_name="games"
    )
    played = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Player(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(
        max_length=50,
        blank=False,
        default='',
        unique=True
    )
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=2,
        default='M'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class PlayerScore(models.Model):
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='scores'
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )
    score = models.IntegerField()
    score_date = models.DateTimeField()

    class Meta:
        ordering = ('-score',)
