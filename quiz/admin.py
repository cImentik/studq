from django.contrib import admin
from quiz.models import Unit, Staff, Answer, Question, Quiz, Current
from django.forms import ModelForm, Textarea

# Register your models here.


admin.site.register(Unit)
admin.site.register(Staff)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Current)