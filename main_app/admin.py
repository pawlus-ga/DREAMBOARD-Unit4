from django.contrib import admin

from .models import Project, Scene, Equipment

admin.site.register(Project)
admin.site.register(Scene)
admin.site.register(Equipment)