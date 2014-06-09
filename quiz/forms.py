from django import forms
from django.forms.extras.widgets import SelectDateWidget

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
FAVORITE_COLORS_CHOICES = (('blue', 'Blue'),
                            ('green', 'Green'),
                            ('black', 'Black'))

#choices=FAVORITE_COLORS_CHOICES
class SimpleForm(forms.Form):
    #birth_year = forms.DateField(widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    favorite_colors = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=())

    def __init__(self, *args, **kwargs):
        super(SimpleForm, self).__init__(*args, **kwargs)
        self.fields['favorite_colors'].choices = (('audio', 'Audio'), ('video', 'Video'))


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    comment = forms.CharField(max_length=9,widget=forms.Textarea)