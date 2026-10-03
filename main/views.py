from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_GET, require_POST
from django.core import serializers
from django.http import HttpResponse, response, JsonResponse
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

# json endpoint buat edu ama hobby
def get_education_json(request):
    education_list = Education.objects.all()

    data = []
    for edu in education_list:
        data.append({
            "pk": str(edu.id),
            "fields": {
                "title": edu.title,
                "started_at": edu.started_at,
                "ended_at": edu.ended_at,
                "is_ongoing": edu.is_ongoing,
            }
        })

    return JsonResponse(data, safe=False)

def get_hobby_json(request):
    hobby_list = Hobby.objects.all()

    data = []
    for hobby in hobby_list:
        data.append({
            "pk": str(hobby.id),
            "fields": {
                "title": hobby.title,
            }
        })

    return JsonResponse(data, safe=False)

def show_project(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Ahmad Rafa Robyan",
        "title_query": title_query,
        "form" : ProjectForm()
    }
    return render(request, "project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

# karena form menjadi popover dan bukan halaman terpisah, ini dipake biar gak perlu ada project/add di url
def project_view(request):
    if request.method == "POST":
        return create_project(request)
    return show_project(request)

def show_experience(request):
    context = {
        "name": "Ahmad Rafa Robyan",
        "experience_list": Experience.objects.all(),
        "experience_form" : ExperienceForm(),
    }
    return render(request, "experience.html", context)

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for exp in experiences:
        data.append({
            "pk": str(exp.id),
            "fields": {
                "title": exp.title,
                "description": exp.description,
                "category": exp.category,
                "is_ongoing": exp.is_ongoing
            }
        })

    return JsonResponse(data, safe=False)

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

# METHOD STAR

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_project")

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
    return redirect("main:show_project")

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

# METHOD MENGHAPUS DATA

@login_required(login_url="/login/")
@require_POST
def delete_edu(request, edu_id):

    if not request.user.is_superuser:
        raise PermissionDenied

    edu = get_object_or_404(Education, pk=edu_id)
    edu.delete()
    messages.success(request, "Edukasi berhasil dihapus!")
    return redirect("main:show_main")

@login_required(login_url="/login/")
@require_POST
def delete_hobby(request, hobby_id):

    if not request.user.is_superuser:
        raise PermissionDenied

    hobby = get_object_or_404(Hobby, pk=hobby_id)
    hobby.delete()
    messages.success(request, "Hobby berhasil dihapus!")
    return redirect("main:show_main")

@login_required(login_url="/login/")
@require_POST
def delete_experience(request, experience_id):

    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
    experience.delete()
    messages.success(request, "Pengalaman berhasil dihapus!")
    return redirect("main:show_experience")

@login_required(login_url="/login/")
@require_POST
def delete_project(request, project_id):

    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    messages.success(request, "Project berhasil dihapus!")
    return redirect("main:show_project")

# METHOD EDIT FORM

@login_required(login_url="/login/")
@require_POST
def edit_edu(request, edu_id):

    if not request.user.is_superuser:
        raise PermissionDenied

    edu = get_object_or_404(Education, pk=edu_id)
    form = EduForm(request.POST, instance=edu)
    if form.is_valid():
        form.save()
        messages.success(request, f"Edukasi '{edu.title}' berhasil diperbarui!")
    return redirect("main:show_main")

@login_required(login_url="/login/")
@require_POST
def edit_hobby(request, hobby_id):

    if not request.user.is_superuser:
        raise PermissionDenied

    hobby = get_object_or_404(Hobby, pk=hobby_id)
    form = HobbyForm(request.POST, instance=hobby)
    if form.is_valid():
        form.save()
        messages.success(request, f"Hobi '{hobby.title}' berhasil diperbarui!")
    return redirect("main:show_main")

@login_required(login_url="/login/")
@require_POST
def edit_project(request, project_id):

    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST, instance=project)
    if form.is_valid():
        form.save()
        messages.success(request, f"Proyek '{project.title}' berhasil diperbarui!")
    return redirect("main:show_project")

@login_required(login_url="/login/")
@require_POST
def edit_experience(request, experience_id):

    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST, instance=experience)
    if form.is_valid():
        form.save()
        messages.success(request, f"Pengalaman '{experience.title}' berhasil diperbarui!")
    return redirect("main:show_experience")
