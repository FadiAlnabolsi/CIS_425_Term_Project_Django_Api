from django import forms
from django.contrib.auth.forms import AuthenticationForm

from snippets.models import Registrations

import datetime

class RegistrationForm(forms.ModelForm):
	GENDER_CHOICES = (
			('M', 'Male'),
			('F', 'Female'),
		)

	COLLEGE_STATUS = (
		('F', 'Freshman'),
		('S', 'Sophomore'),
		('J', 'Junior'),
		('Sr', 'Senior'),
		('Sr1', 'Older'),
		)

	dob_day = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)])
	dob_month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)])
	dob_year = forms.ChoiceField(choices=[(x, x) for x in range(1960, 2006)])
	gender = forms.ChoiceField(choices=GENDER_CHOICES)
	collegeStatus = forms.ChoiceField(choices=COLLEGE_STATUS)

	date = datetime.date.today()
	phoneNumber = forms.RegexField(regex=r'^\+?1?\d{9,15}$', )

	registration_day = forms.CharField(
		widget=forms.TextInput(attrs={'readonly':'readonly'})
		)

	registration_month = forms.CharField(
		widget=forms.TextInput(attrs={'readonly':'readonly'})
		)

	registration_year = forms.CharField(
		widget=forms.TextInput(attrs={'readonly':'readonly'})
		)

	emailaddress = forms.CharField()

	class Meta:
		model = Registrations
		fields = ('firstName', 'lastName', 
			      'studentNumber', 'emailaddress', 
			      'phoneNumber', 'dob_day',
			      'dob_month', 'dob_year', 
                  'registration_day', 'registration_month',
                  'registration_year', 'gender',
                  'collegeStatus', 'cumGpa', 
                  'numCredits') 