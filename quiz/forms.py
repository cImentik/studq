# -*- coding: utf-8 -*-
from django import forms
from quiz.models import Current


class CurrentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        question_name = kwargs.pop('qc', None)
        super(CurrentForm, self).__init__(*args, **kwargs)
        self.fields['answer'].label = question_name

    class Meta:
        model = Current
        fields = ['answer']
        widgets = {
            'answer': forms.RadioSelect()
        }