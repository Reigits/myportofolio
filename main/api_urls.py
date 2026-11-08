from django.urls import path
from main import api_views

app_name = "api"
urlpatterns = [
    # projek
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", api_views.project_star, name="project-star"),

    # pengalaman
    path("experiences/", api_views.experience_list, name="experience-list"),
    path("experiences/<uuid:experience_id>/", api_views.experience_detail, name="experience-detail"),

    # edukasi
    path("education/", api_views.education_list, name="education-list"),
    path("education/<uuid:edu_id>/", api_views.education_detail, name="education-detail"),

    # hobi
    path("hobbies/", api_views.hobby_list, name="hobby-list"),
    path("hobbies/<uuid:hobby_id>/", api_views.hobby_detail, name="hobby-detail"),
]
