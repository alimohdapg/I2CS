from django import forms
from .models import methods_of_contact
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, Evaluations


class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=254)
    password = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput)


class SignUpForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=150)
    last_name = forms.CharField(label='Last Name', max_length=150)
    phone_num = forms.CharField(label='Phone Number', max_length=150)
    email = forms.CharField(label='Email', max_length=45)
    password1 = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', max_length=128, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email Already Exists.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        user = User(email=self.cleaned_data.get('email'), password=password1, first_name=self.cleaned_data.get('first_name'),
                    last_name=self.cleaned_data.get('last_name'), phone_num=self.cleaned_data.get('phone_num'))
        try:
            validate_password(password1, user=user)
        except ValidationError as e:
            raise forms.ValidationError(e.error_list)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2


class RequestEvaluationForm(forms.ModelForm):
    details = forms.CharField(label='Details of Object and Request', widget=forms.Textarea())
    image = forms.ImageField(label='Object Photo')
    contact_method = forms.ChoiceField(label='Preferred Method of Contact', choices=methods_of_contact)

    class Meta:
        model = Evaluations
        fields = ['details', 'image', 'contact_method']
