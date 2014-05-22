from django.contrib import admin
from quiz.models import Unit, Staff, Answer, Question
from django.forms import ModelForm, Textarea

# Register your models here.


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['content']}),
    ]
    inlines = [AnswerInline]

admin.site.register(Unit)
admin.site.register(Staff)
#admin.site.register(Answer)
admin.site.register(Question, QuestionAdmin)