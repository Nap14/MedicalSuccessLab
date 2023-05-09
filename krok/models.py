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


class Test(models.Model):
    STEP = [(i, str(i)) for i in range(1, 4)]

    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)
    year = models.IntegerField(
        validators=(validators.MinValueValidator(limit_value=2001)),
    )
    step = models.IntegerField(choices=STEP)
    params = models.ManyToManyField(Param)
    english = models.BooleanField(default=False)

    class Meta:
        unique_together = (("profession", "year", "step", "params"),)
        default_related_name = "tests"
        ordering = ["-year"]
        indexes = (models.Index(fields=("step", "year"), name="step_year_idx"),)
