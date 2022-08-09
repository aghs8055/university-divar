from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    error_messages = {
        'password_mismatch': 'Password and repeat password are not the same!'
    }

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        error_messages = {
            'username': {
                'unique': 'Your username is exists in system!'
            }
        }


class ContactUsForm(forms.Form):
    title = forms.CharField(required=True)
    text = forms.CharField(required=True, widget=forms.Textarea, max_length=250, min_length=10)
    email = forms.EmailField(required=True)

    def send_mail(self):
        send_mail(self.cleaned_data.get('title'),
                  f'{self.cleaned_data.get("text")} \n {self.cleaned_data.get("email")}', 'aghs8055@gmail.com',
                  ['aghs8055@gmail.com'], fail_silently=False)


class ProfileSettingsForm(forms.Form):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    image = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    gender = forms.ChoiceField(choices=(('', '-----'), ('M', 'Male'), ('F', 'Female')), required=False)
    user_type = forms.ChoiceField(choices=(('', '-----'), ('S', 'Student'), ('T', 'Teacher')), required=False)


