from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_GET, require_POST
from django.core import serializers
from django.http import HttpResponse, response
from django.shortcuts import get_object_or_404, redirect, render
import datetime

from main.models import *
from main.forms import *

# METHOD MENAMPILKAN

def show_main(request):
    # form buat popover
    edu_form = EduForm(request.POST or None)
    hobby_form = HobbyForm(request.POST or None)

    # last login buat ditampilin
    last_login = request.COOKIES.get('last_login', 'Belom ada sesi login / Cookie tidak ditemukan')

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("/admin/login/")

        form_type = request.POST.get("form_type")

        if form_type == "education" and edu_form.is_valid():
            edu_form.save()
            messages.success(request, "Edukasi baru berhasil ditambahkan!")
            return redirect("main:show_main")

        elif form_type == "hobby" and hobby_form.is_valid():
            hobby_form.save()
            messages.success(request, "Hobi baru berhasil ditambahkan!")
            return redirect("main:show_main")

    context = {
        "name": "Ahmad Rafa Robyan",
        "npm": "2506620721",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "An individual who happens to be a student at CSUI and really likes many things, primarily tech-stuff."
        ),
        "education_list" : Education.objects.all(),
        "hobby_list" : Hobby.objects.all(),
        "edu_form" : EduForm(),
        "hobby_form" : HobbyForm(),
        "last_login": last_login,
    }
    return render(request, "index.html", context)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Ahmad Rafa Robyan",
        "project_list": projects,
        "title_query": title_query,
        "form" : ProjectForm()
    }
    return render(request, "project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

# karena form menjadi popover dan bukan halaman terpisah, ini dipake biar gak perlu ada project/add di url
def project_view(request):
    if request.method == "POST":
        return create_project(request)
    return show_projects(request)

def show_experience(request):
    context = {
        "name": "Ahmad Rafa Robyan",
        "experience_list": Experience.objects.all(),
        "experience_form" : ExperienceForm(),
    }
    return render(request, "experience.html", context)

def experience_view(request):
    if request.method == "POST":
        return create_experience(request)
    return show_experience(request)

# METHOD REGISTER/LOGIN/LOGOUT

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Ahmad Rafa Robyan",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Ahmad Rafa Robyan",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# METHOD MEMBUAT FORM

@login_required(login_url="/login/")
@require_POST
def create_edu(request):

    if not request.user.is_superuser:
        raise PermissionDenied

    form = EduForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Edukasi baru berhasil ditambahkan!")

    context = {
        "name": "Ahmad Rafa Robyan",
        "form": form,
    }
    return redirect("main:show_main_edu")

@login_required(login_url="/login/")
@require_POST
def create_hobby(request):

    if not request.user.is_superuser:
        raise PermissionDenied

    form = HobbyForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Hobi baru berhasil ditambahkan!")

    context = {
        "name": "Ahmad Rafa Robyan",
        "form": form,
    }
    return redirect("main:show_main_hobby")

@login_required(login_url="/login/")
@require_POST
def create_experience(request):

    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)

    if form.is_valid:
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")

    context = {
        "name": "Ahmad Rafa Robyan",
        "form": form,
    }
    return redirect("main:show_experience")

@login_required(login_url="/login/")
@require_POST
def create_project(request):

    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")

    context = {
        "name": "Ahmad Rafa Robyan",
        "form": form,
    }
    return redirect("main:show_projects")

# METHOD MENGHAPUS DATA

@login_required(login_url="/login/")
@require_POST
def delete_edu(request, edu_id):
    edu = get_object_or_404(Education, pk=edu_id)
    edu.delete()
    messages.success(request, "Edukasi berhasil dihapus!")
    return redirect("main:show_main")

@login_required(login_url="/login/")
@require_POST
def delete_hobby(request, hobby_id):
    hobby = get_object_or_404(Hobby, pk=hobby_id)
    hobby.delete()
    messages.success(request, "Hobby berhasil dihapus!")
    return redirect("main:show_main")

@login_required(login_url="/login/")
@require_POST
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    experience.delete()
    messages.success(request, "Pengalaman berhasil dihapus!")
    return redirect("main:show_experience")

@login_required(login_url="/login/")
@require_POST
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    messages.success(request, "Project berhasil dihapus!")
    return redirect("main:show_projects")

# METHOD EDIT FORM

@login_required(login_url="/login/")
@require_POST
def edit_edu(request, edu_id):
    edu = get_object_or_404(Education, pk=edu_id)
    form = EduForm(request.POST, instance=edu)
    if form.is_valid():
        form.save()
        messages.success(request, f"Edukasi '{edu.title}' berhasil diperbarui!")
    return redirect("main:show_main")

@login_required(login_url="/login/")
@require_POST
def edit_hobby(request, hobby_id):
    hobby = get_object_or_404(Hobby, pk=hobby_id)
    form = HobbyForm(request.POST, instance=hobby)
    if form.is_valid():
        form.save()
        messages.success(request, f"Hobi '{hobby.title}' berhasil diperbarui!")
    return redirect("main:show_main")

@login_required(login_url="/login/")
@require_POST
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST, instance=project)
    if form.is_valid():
        form.save()
        messages.success(request, f"Proyek '{project.title}' berhasil diperbarui!")
    return redirect("main:show_projects")

@login_required(login_url="/login/")
@require_POST
def edit_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST, instance=experience)
    if form.is_valid():
        form.save()
        messages.success(request, f"Pengalaman '{experience.title}' berhasil diperbarui!")
    return redirect("main:show_experience")
