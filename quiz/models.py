# -*- coding: utf-8 -*-
from django.db import models


class Unit(models.Model):
    name = models.CharField('Наз. кафедры', max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'


class Staff(models.Model):
    name = models.CharField('ФИО', max_length=50)
    unit = models.ForeignKey(Unit, verbose_name='Кафедра')
    available = models.BooleanField('Доступен для тестирования', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Преподователь'
        verbose_name_plural = 'Преподователи'


class Question(models.Model):
    content = models.TextField('Текст вопроса')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    content = models.TextField('Текст ответа')
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


#Модель под вопросом... посмотреть
class Quiz(models.Model):
    staff = models.ForeignKey(Staff, verbose_name='Преподователь')
    question = models.ForeignKey(Question, verbose_name='Вопрос')
    result = models.FloatField('Результат', default=0.0)

    def __str__(self):
        return "Quiz"

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Current(models.Model):
    session_key = models.CharField("Сессия (ключ)", max_length=32)
    staff = models.ForeignKey(Staff, verbose_name='Преподователь')
    question = models.ForeignKey(Question, verbose_name='Вопрос')
    answer = models.ForeignKey(Answer, blank=False, default=-1, verbose_name='Ответ')

    def __str__(self):
        return self.session_key

    class Meta:
        verbose_name = 'Текущий опрос'
        verbose_name_plural = 'Текущие опросы'