from django.urls import path
from main import api_views

app_name = "api"
urlpatterns = [
    path("projects/", api_views.project_list, name="project-list"),
]
