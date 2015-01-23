# -*- coding: utf-8 -*-
from django import forms
from quiz.models import Current, Answer
from django.forms.extras.widgets import SelectDateWidget

GENDER_MALE = 0
GENDER_FEMALE = 1
CHOICES_GENDER = ((GENDER_MALE, "Male"),
                  (GENDER_FEMALE, "Female"))

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
FAVORITE_COLORS_CHOICES = (('blue', 'Blue'),
                           ('green', 'Green'),
                           ('black', 'Black'))

#choices=FAVORITE_COLORS_CHOICES


class SimpleForm(forms.Form):
    #birth_year = forms.DateField(widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    #mylabel = forms.CharField(widget=forms.CharField)
    question_id = forms.CharField(required=False, widget=forms.HiddenInput)
    answers = forms.ChoiceField(label=u'Answers', required=False, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):

        answers = kwargs.pop('an', None)
        question = kwargs.pop('q', None)
        super(SimpleForm, self).__init__(*args, **kwargs)
        #d1 = dict(audio='Audio', video='Video', other='Other')
        #d2 = [('audio', 'Audio'), ('video', 'Video')]
        d1 = []
        d1.append(('audio', 'Audio'))
        d1.append(('video', 'Video'))

        #assert False
        self.fields['answers'].choices = answers #[('audio', 'Audio'), ('video', 'Video')]#{('audio', 'Audio'), ('video', 'Video')}
        #self.fields['mylabel'] = question.content


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    comment = forms.CharField(max_length=9, widget=forms.Textarea)


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