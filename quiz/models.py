from django.db import models

# Create your models here.


class Staff(models.Model):
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=10)


class Question(models.Model):
    content = models.TextField()


class Answer(models.TextField):
    content = models.TextField()
    question_id = models.ForeignKey(Question)
