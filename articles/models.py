from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


class ArticleColumn(models.Model):

    title = models.CharField(max_length=100, blank=True)

    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class ArticlePost(models.Model):
    # the author of the article, on_delete means the way when the data is deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # the title of the article
    title = models.CharField(max_length=200)

    # the body of the article
    body = models.TextField()

    # the time when the article was posted, default means take the current time
    created_time = models.DateTimeField(default=timezone.now)

    # the update time of the article , auto_now default writes current time
    updated_time = models.DateTimeField(auto_now=True)

    # total numbers of views
    total_views = models.PositiveIntegerField(default=0)

    # tags of the article
    tags = TaggableManager(blank=True)

    column = models.ForeignKey(
            ArticleColumn,
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='article'
            )

    # internal class , defines the meta data
    class Meta:
        # means the posted articles should be ordered by the time they created reverselly
        ordering = ('-created_time',)


    # recommended method when this object is called ,return a human readable string
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:article_detail', args=[self.id])
