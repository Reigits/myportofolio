import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Education, Experience, Hobby, Project


# =============================================================================
# PROJECT API TESTS
# =============================================================================
class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": "Python",
            "project_url": "https://example.com/", "project_image_url": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# =============================================================================
# EXPERIENCE API TESTS
# =============================================================================
class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com"
        )
        self.editor_group = Group.objects.create(name="Editor")
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(self.editor_group)

        self.user = User.objects.create_user(username="user", password="test-password")

        self.experience = Experience.objects.create(
            title="Software Engineer",
            description="Developing web services.",
            category="full-time",
            started_at="2026-01-01T00:00:00Z",
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.payload = {
            "title": "Backend Intern",
            "description": "Building Django APIs.",
            "category": "internship",
            "started_at": "2026-06-01T00:00:00Z",
            "ended_at": None,
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertTrue(response.data[0]["is_ongoing"])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_filter(self):
        response = self.client.get(self.list_url, {"title": "Engineer"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "non-existent"})
        self.assertEqual(response.data, [])

    def test_guest_and_user_cannot_write(self):
        for user in (None, self.user):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Hacked"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Software Engineer")

    def test_editor_can_patch_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        # Editor fails on POST (Create)
        res_post = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(res_post.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

        # Editor succeeds on PATCH (Update)
        res_patch = self.client.patch(self.detail_url, {"title": "Lead Engineer"}, format="json")
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Lead Engineer")

        # Editor fails on DELETE
        res_delete = self.client.delete(self.detail_url)
        self.assertEqual(res_delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Experience.objects.filter(pk=self.experience.id).exists())

    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        # Create
        res_post = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(res_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Experience.objects.count(), 2)

        # Delete
        res_delete = self.client.delete(self.detail_url)
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Experience.objects.filter(pk=self.experience.id).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.post(self.list_url, {**self.payload, "title": "   "}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", res.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_csrf_protection_enforced(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        res = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)


# =============================================================================
# EDUCATION API TESTS
# =============================================================================
class EducationAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com"
        )
        self.editor_group = Group.objects.create(name="Editor")
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(self.editor_group)

        self.user = User.objects.create_user(username="user", password="test-password")

        self.edu = Education.objects.create(title="Universitas Indonesia", started_at=2024, ended_at=2028)
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.edu.id])
        self.payload = {"title": "SMA High School", "started_at": 2021, "ended_at": 2024}

    def test_public_list_and_detail(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["id"], str(self.edu.id))
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_guest_and_user_cannot_write(self):
        for u in (None, self.user):
            self.client.force_authenticate(user=u)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Hacked"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Education.objects.count(), 1)

    def test_editor_can_patch_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)

        res_patch = self.client.patch(self.detail_url, {"title": "UI Fasilkom"}, format="json")
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)
        self.edu.refresh_from_db()
        self.assertEqual(self.edu.title, "UI Fasilkom")

        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertTrue(Education.objects.filter(pk=self.edu.id).exists())

    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        res_post = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(res_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Education.objects.count(), 2)

        res_delete = self.client.delete(self.detail_url)
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Education.objects.filter(pk=self.edu.id).exists())

    def test_end_year_before_start_year_validation(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.post(
            self.list_url, {"title": "Invalid Edu", "started_at": 2025, "ended_at": 2020}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ended_at", res.data)
        self.assertEqual(Education.objects.count(), 1)


# =============================================================================
# HOBBY API TESTS
# =============================================================================
class HobbyAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com"
        )
        self.editor_group = Group.objects.create(name="Editor")
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(self.editor_group)

        self.user = User.objects.create_user(username="user", password="test-password")

        self.hobby = Hobby.objects.create(title="Coding")
        self.list_url = reverse("api:hobby-list")
        self.detail_url = reverse("api:hobby-detail", args=[self.hobby.id])
        self.payload = {"title": "Gaming"}

    def test_public_list_and_detail(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["id"], str(self.hobby.id))

    def test_guest_and_user_cannot_write(self):
        for u in (None, self.user):
            self.client.force_authenticate(user=u)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Hacked"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Hobby.objects.count(), 1)

    def test_editor_can_patch_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)

        res_patch = self.client.patch(self.detail_url, {"title": "Competitive Programming"}, format="json")
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)
        self.hobby.refresh_from_db()
        self.assertEqual(self.hobby.title, "Competitive Programming")

        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertTrue(Hobby.objects.filter(pk=self.hobby.id).exists())

    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        res_post = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(res_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hobby.objects.count(), 2)

        res_delete = self.client.delete(self.detail_url)
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Hobby.objects.filter(pk=self.hobby.id).exists())
