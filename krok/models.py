from django.core import validators, exceptions
from django.db import models

from . import base_models


class Profession(base_models.BaseNameClass):
    pass


class Param(base_models.BaseNameClass):
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


class Explanation(models.Model):
    text = models.CharField(max_length=500)


class Question(models.Model):
    text = models.CharField(max_length=500)
    test = models.ForeignKey(Test, on_delete=models.SET_NULL)
    explanation = models.ForeignKey(Explanation, on_delete=models.SET_NULL)


class QuestionTranslation(base_models.BaseTranslation):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)


class Variant(models.Model):
    text = models.CharField(max_length=100)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="variants"
    )
    is_correct = models.BooleanField()

    def clean(self):
        super(Variant, self).clean()
        if self.is_correct and self.question.variants.filter(is_correct=True).exists():
            raise exceptions.ValidationError("Only one variant can be correct")

    def save(
        self, *args, **kwargs
    ):
        self.full_clean()
        super(Variant, self).save(*args, **kwargs)


class VariantTranslation(base_models.BaseTranslation):
    variant = models.OneToOneField(Variant, on_delete=models.CASCADE)
