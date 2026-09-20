from django.urls import path

from main.views import *

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", experience_view, name="show_experience"),
    path("projects/", project_view , name="show_projects"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("edu/<uuid:edu_id>/delete/", delete_edu, name="delete_edu"),
    path("hobby/<uuid:hobby_id>/delete/", delete_hobby, name="delete_hobby"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("education/<uuid:edu_id>/edit/", edit_edu, name="edit_edu"),
    path("hobby/<uuid:hobby_id>/edit/", edit_hobby, name="edit_hobby"),
    path("projects/<uuid:project_id>/edit/", edit_project, name="edit_project"),
    path("experience/<uuid:experience_id>/edit/", edit_experience, name="edit_experience"),
]
