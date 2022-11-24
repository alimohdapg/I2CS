from django import forms
from .models import methods_of_contact


class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=254)
    password = forms.CharField(label='Password', max_length=128, min_length=8)


class SignUpForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=150)
    last_name = forms.CharField(label='Last Name', max_length=150)
    phone_num = forms.CharField(label='Phone Number', max_length=150)
    email = forms.CharField(label='Email', max_length=45)
    password = forms.CharField(label='Password', max_length=128, min_length=8)


class RequestEvaluationForm(forms.Form):
    details = forms.CharField(label='Details of Object and Request', widget=forms.Textarea())
    image = forms.ImageField(label='Object Photo')
    contact_method = forms.ChoiceField(label='Preferred Method of Contact', choices=methods_of_contact)
