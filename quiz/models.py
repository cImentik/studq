# -*- coding: utf-8 -*-
from django.db import models


class Unit(models.Model):
    name = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField(max_length=50)
    unit = models.ForeignKey(Unit)
    available = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    content = models.TextField()

    def __unicode__(self):
        return self.content


class Answer(models.Model):
    content = models.TextField()
    weight = models.IntegerField(default=0)

    def __unicode__(self):
        return self.content


class Quiz(models.Model):
    staff_id = models.ForeignKey(Staff)
    question_id = models.ForeignKey(Question)
    result = models.FloatField(default=0.0)

    def __unicode__(self):
        return "Quiz"


class Current(models.Model):
    session_key = models.CharField(max_length=32)
    staff_id = models.ForeignKey(Staff)
    question_id = models.ForeignKey(Question)
    answer_id = models.ForeignKey(Answer)

    def __unicode__(self):
        return  "Current"