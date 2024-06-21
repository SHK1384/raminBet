from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class PredictForm(forms.Form):
    team_1_score = forms.IntegerField()
    team_2_score = forms.IntegerField()

class FinalistPredictForm(forms.Form):
    team_1 = forms.ModelChoiceField(queryset=Team.objects.all())
    team_2 = forms.ModelChoiceField(queryset=Team.objects.all())

class ChampionsForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all())
