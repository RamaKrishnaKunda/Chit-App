from django import forms
from chit_app.models import *
import datetime

class AddChitForm(forms.ModelForm):
    class Meta:
        model = Chit
        exclude = ['people_present', 'user']

    def clean(self):
        form_data = self.cleaned_data
        if form_data['month'] <= 0 or form_data['month'] > 12:
            self._errors['error'] = 'Invalid Month'
        if form_data['year'] != datetime.datetime.now().year:
            self._errors['error'] = 'Year should be current year'
        if form_data['amount'] <= 0 :
            self._errors['error'] = 'Invalid amount'
        if form_data['number_of_months'] <= 0:
            self._errors['error'] = 'Invalid number of months'
        return form_data


class AddPersonForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        # required=True,
        label='Username',
        widget=forms.TextInput()
    )
    num_of_chits = forms.IntegerField(
        label='Number of Chits',
        widget=forms.NumberInput(),
        # required=True
    )