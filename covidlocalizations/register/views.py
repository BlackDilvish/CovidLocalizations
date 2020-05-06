from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from .forms import RegisterForm

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})

def loggedout(response):
    return render(response, "register/loggedout.html", {})
