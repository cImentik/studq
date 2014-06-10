from django import forms
from django.forms.extras.widgets import SelectDateWidget

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
FAVORITE_COLORS_CHOICES = (('blue', 'Blue'),
                           ('green', 'Green'),
                           ('black', 'Black'))

#choices=FAVORITE_COLORS_CHOICES
class SimpleForm(forms.Form):
    #birth_year = forms.DateField(widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    answers = forms.ChoiceField(label=u'Answers', required=False, widget=forms.RadioSelect, choices=())

    def __init__(self, *args, **kwargs):
        #assert False
        answers = kwargs.pop('an', None)
        super(SimpleForm, self).__init__(*args, **kwargs)
        self.fields['answers'].choices = {'content': u'\u0432\u0441\u0435\u0433\u0434\u0430'} #answers #(('audio', 'Audio'), ('video', 'Video'))


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    comment = forms.CharField(max_length=9,widget=forms.Textarea)