from django.urls import path

from main.views import show_main, show_experience, create_project, show_projects

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("projects/add/", create_project, name = "create_project"),
    path("projects/", show_projects, name="show_projects"),
]
