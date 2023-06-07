from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CreateTask
from .models import Task


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"user_creation_form": UserCreationForm})
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                return redirect("login")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {
                        "user_creation_form": UserCreationForm,
                        "error": "username already exists",
                    },
                )
        else:
            return render(
                request,
                "signup.html",
                {
                    "user_creation_form": UserCreationForm,
                    "error": "passwords does not match",
                },
            )


def signin(request):
    if request.method == "GET":
        return render(
            request, "login.html", {"authentication_form": AuthenticationForm}
        )
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "login.html",
                {
                    "authentication_form": AuthenticationForm,
                    "error": "username or password is incorrect",
                },
            )
        else:
            login(request, user=user)
            return redirect("tasks")


@login_required(login_url="login")
def signout(request):
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "tasks.html", {"tasks": tasks})


@login_required(login_url="login")
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"create_task": CreateTask})
    if request.method == "POST":
        form = CreateTask(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("tasks")
        else:
            return render(
                request,
                "create_task.html",
                {"create_task": CreateTask, "error": "Error creando la tarea!"},
            )


@login_required(login_url="login")
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id)
        form = CreateTask(instance=task)
        return render(request, "task_detail.html", {"task": task, "form": form})
    else:
        task = get_object_or_404(Task, pk=task_id)
        form = CreateTask(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks")
        else:
            task = get_object_or_404(Task, pk=task_id)
            form = CreateTask(instance=task)
            return render(
                request,
                "task_detail.html",
                {"task": task, "form": form, "error": "Error en la actualizacion"},
            )


@login_required(login_url="login")
def delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=task_id)
        task.delete()
        return redirect("tasks")
