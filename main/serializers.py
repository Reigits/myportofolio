from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import *


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack",
            "project_url", "project_image_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())

class ExperienceSerializer(serializers.ModelSerializer):
    is_ongoing = serializers.BooleanField(read_only=True)

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
            "is_ongoing",
        ]
        read_only_fields = ["id", "is_ongoing"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

class EducationSerializer(serializers.ModelSerializer):
    is_ongoing = serializers.BooleanField(read_only=True)

    class Meta:
        model = Education
        fields = [
            "id",
            "title",
            "started_at",
            "ended_at",
            "is_ongoing",
        ]
        read_only_fields = ["id", "is_ongoing"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate(self, data):
        started_at = data.get("started_at")
        ended_at = data.get("ended_at")

        if ended_at is not None and started_at is not None and ended_at < started_at:
            raise serializers.ValidationError({
                "ended_at": "End year cannot be earlier than start year."
            })
        return data

class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = [
            "id",
            "title",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value
