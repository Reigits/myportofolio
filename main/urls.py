from django.urls import path

from main.views import *

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    # project
    path("project/", project_view , name="show_project"),
    path("project/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path("project/<uuid:project_id>/edit/", edit_project, name="edit_project"),
    path("project/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("api/project/", get_projects_json, name="get_projects_json"),
    path(
    "projects/<uuid:project_id>/star/",
    toggle_star,
    name="toggle_star"),

    # experience
    path("experience/", experience_view, name="show_experience"),
    path("experience/<uuid:experience_id>/edit/", edit_experience, name="edit_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),

    # edu/hobby
    path("edu/<uuid:edu_id>/delete/", delete_edu, name="delete_edu"),
    path("hobby/<uuid:hobby_id>/delete/", delete_hobby, name="delete_hobby"),
    path("education/<uuid:edu_id>/edit/", edit_edu, name="edit_edu"),
    path("hobby/<uuid:hobby_id>/edit/", edit_hobby, name="edit_hobby"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]
