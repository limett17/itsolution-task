from django.db import models
from django.contrib.auth.models import User


# model for sources of quotes
class Source(models.Model):
    SOURCE_TYPES = (
        ('КНИГА', 'Книга'),
        ('МУЗЫКА', 'Музыка'),
        ('ФИЛЬМ', 'Фильм'),
        ('СЕРИАЛ', 'Сериал'),
        ('МУЛЬТФИЛЬМ', 'Мультфильм'),
        ('ДРУГОЕ', 'Другое'),
    )
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=SOURCE_TYPES, default='OTHER')

    class Meta:
        unique_together = ('name', 'type')


# model for quotes
class Quote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    quote = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    prob_rate = models.PositiveIntegerField(default=-1)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class ViewCount(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('quote', 'user')


class RatingCount(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(choices=[(1, 'Нравится'), (-1, 'Не нравится')])

    class Meta:
        unique_together = ('quote', 'user')
        ordering = ('-timestamp',)
        indexes = [models.Index(fields=['-timestamp', 'value'])]
