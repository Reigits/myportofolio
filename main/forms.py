from pydoc import text
from random import choices

from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput, Select, DateTimeInput

from main.models import *

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

class EduForm(ModelForm):
    class Meta:
        model = Education
        fields = [
                "title",
                "started_at",
                "ended_at"
            ]

        labels = {
                "title" : "Nama Sekolah",
                "started_at" : "Tahun Mulai",
                "ended_at" : "Tahun Selesai"
            }

        widgets = {
                "title" : TextInput(
                    attrs = {
                        "placeholder" : "Harvard",
                        "maxlength" : 255,
                        }
                    ),
                "started_at" : NumberInput(
                    attrs = {
                        "placeholder" : 1984,
                        }
                    ),
                "ended_at" : NumberInput(
                    attrs = {
                        "placeholder" : 2045,
                        }
                    )
            }

class HobbyForm(ModelForm):
    class Meta:
        fields = [
                "title",
            ]

        labels = {
                "title" : "Hobby yang Kamu Miliki",
            }

        widgets = {
                "title" : TextInput(
                    attrs = {
                        "placeholder" : "Coding",
                        "maxlength" : 255,
                        }
                    ),     
            }

class ExperienceForm(ModelForm):
    class Meta:
        fields = [
                "title",
                "description",
                "category",
                "thumbnail",
                "started_at",
                "ended_at",
            ]
        
        labels = {
                "title" : "Nama Pengalaman",
                "description" : "Deskripsi Pengalaman",
                "category" : "Tipe Pengalaman",
                "thumbnail" : "Gambar Pengalaman",
                "started_at" : "Tanggal Mulai",
                "ended_at" : "Tanggal Berakhir",
            }

        widgets = {
                "title" : TextInput(
                    attrs = {
                        "placeholder" : "Certified Person",
                        "maxlength" : 255,
                        }
                    ),
                "description" : TextInput(
                    attrs = {
                        "placeholder" : "Orang yang Handal",
                        "maxlength" : 255,
                        }
                    ),
                "category" : Select(
                    choices = Experience.EXPERIENCE_CHOICES,
                    attrs = {
                        "placeholder" : "Freelance",
                        }
                    ),
                "started_at": DateTimeInput(
                        attrs={
                            "type": "datetime-local",
                        }
                    ),
                "ended_at": DateTimeInput(
                        attrs={
                            "type": "datetime-local",
                        }
                    ),
            }
