from django.db import models

# Create your models here.


class Unit(models.Model):
    name = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField(max_length=50)
    unit = models.ForeignKey(Unit)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    content = models.TextField()

    def __unicode__(self):
        return self.content


class Answer(models.Model):
    content = models.TextField()
    question_id = models.ForeignKey(Question)

    def __unicode__(self):
        return self.content