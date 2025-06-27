from django.db import models


# model for sources of quotes
class Source(models.Model):
    SOURCE_TYPES = (
        ('BOOK', 'Book'),
        ('MUSIC', 'Music'),
        ('MOVIE', 'Movie'),
        ('SERIES', 'Series'),
        ('CARTOON', 'Cartoon'),
        ('OTHER', 'Other'),
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
    prob_rate = models.FloatField(default=0.01)
    # def get_view_count(self):
    #     return self.views.count()


class ViewCount(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(verbose_name='IP Address')

    class Meta:
        unique_together = ('quote', 'ip_address')
