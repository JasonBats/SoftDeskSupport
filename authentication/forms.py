from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "birth_date", "can_be_contacted")
        widgets = {
            "birth_date": forms.DateInput(format="%d/%m/%Y", attrs={"type": "date"})
        }
