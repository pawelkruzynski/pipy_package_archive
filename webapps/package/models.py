from django.db import models


class Package(models.Model):
    guid = models.CharField(max_length=255, unique=True)
    link = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    author_email = models.EmailField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(
        'Tag',
        related_name='packages',
        blank=True,
    )
    current_version = models.CharField(max_length=50)
    maintainer = models.CharField(max_length=100)

    @property
    def get_tags(self):
        return ', '.join(tag.name for tag in self.tags.all())


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
