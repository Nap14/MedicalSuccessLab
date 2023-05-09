from django.core import validators
from django.db import models


class BaseNameClass(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Profession(BaseNameClass):
    pass


class Param(BaseNameClass):
    pass
