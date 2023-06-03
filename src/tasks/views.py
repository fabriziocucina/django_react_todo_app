from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


def signup(requests):
    return render(requests, "signup.html", {"user_creation_form": UserCreationForm})
