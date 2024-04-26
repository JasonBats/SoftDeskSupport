from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login
from django.conf import settings
from SoftDeskSupport.utils import get_user_age, define_can_be_shared


def signup(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.age = get_user_age(user.birth_date)
            user.can_be_shared = define_can_be_shared(user.age)
            user.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})
