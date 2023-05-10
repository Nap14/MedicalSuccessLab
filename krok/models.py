from django.contrib.auth.models import AbstractUser
from django.core import validators, exceptions
from django.db import models

from . import base_models


class User(AbstractUser):
    email = models.EmailField()
    profile_type = models.ForeignKey(
        "ProfileType", on_delete=models.SET_DEFAULT, default=1
    )

    def __str__(self):
        return self.username


class ProfileType(models.Model):
    name = models.CharField(max_length=100)


class Profession(base_models.BaseNameClass):
    pass


class Param(base_models.BaseNameClass):
    text = models.CharField(max_length=50)


class Test(models.Model):
    STEP = [(i, str(i)) for i in range(1, 4)]

    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)
    year = models.IntegerField(
        validators=(validators.MinValueValidator(limit_value=2001),)
    )
    step = models.IntegerField(choices=STEP)
    params = models.ManyToManyField(Param)
    english = models.BooleanField(default=False)

    class Meta:
        default_related_name = "tests"
        ordering = ["-year"]
        indexes = (models.Index(fields=("step", "year"), name="step_year_idx"),)


class Explanation(models.Model):
    text = models.CharField(max_length=500)


class Question(models.Model):
    text = models.CharField(max_length=500)
    test = models.ForeignKey(
        Test, on_delete=models.SET_NULL, related_name="questions", null=True
    )
    explanation = models.ForeignKey(
        Explanation, on_delete=models.SET_NULL, related_name="questions", null=True
    )


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

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Variant, self).save(*args, **kwargs)


class VariantTranslation(base_models.BaseTranslation):
    variant = models.OneToOneField(Variant, on_delete=models.CASCADE)


class TestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attempts")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="attempts")
    mistakes = models.ManyToManyField(Question)
    result = models.DecimalField(
        validators=(validators.MinValueValidator(0), validators.MaxValueValidator(100)),
        decimal_places=2,
        max_digits=5,
    )


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "comments"
        ordering = ["-created_date"]
