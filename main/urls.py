from django.urls import path

from main.views import *

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("projects/", project_view , name="show_projects"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),
]
