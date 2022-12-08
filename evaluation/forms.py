from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth import password_validation
from .models import methods_of_contact
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, Evaluations
from django.core import validators


class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=254)
    password = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        try:
            existing = User.objects.get(email=email)
        except User.DoesNotExist:
            existing = None
        if existing and not existing.is_active:
            raise ValidationError("Please verify email.")
        return email


class SignUpForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=150)
    last_name = forms.CharField(label='Last Name', max_length=150)
    phone_num = forms.CharField(label='Phone Number', max_length=150)
    email = forms.CharField(label='Email', max_length=45,
                            validators=[validators.EmailValidator(message="Invalid Email")])
    password1 = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Confirm Password', max_length=128, widget=forms.PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email Already Exists.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        user = User(email=self.cleaned_data.get('email'), password=password1,
                    first_name=self.cleaned_data.get('first_name'),
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
