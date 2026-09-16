from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import *
from main.forms import ProjectForm

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Ahmad Rafa Robyan",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def show_projects(request):
    context = {
        "name": "Ahmad Rafa Robyan",
        "project_list": Project.objects.all(),
    }
    return render(request, "project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def show_main(request):
    context = {
        "name": "Ahmad Rafa Robyan",
        "npm": "2506620721",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "An individual who happens to be a student at CSUI and really likes many things, primarily tech-stuff."
        ),
        "education_list" : Education.objects.all(),
        "hobby_list" : Hobby.objects.all(),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Ahmad Rafa Robyan",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


