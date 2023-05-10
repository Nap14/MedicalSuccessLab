from django.db import models


class BaseNameClass(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class BaseTranslation(models.Model):
    text = models.TextField()

    class Meta:
        default_related_name = "translation"
