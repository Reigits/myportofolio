from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Ahmad Rafa Robyan",
        "npm": "2506620721",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "An individual who happens to be a student at CSUI and really likes many things, primarily tech-stuff."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Ahmad Rafa Robyan",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)
