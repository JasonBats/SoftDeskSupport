from django.contrib import admin
from SoftDeskApp.models import Project, Issue, Comment, Contributor


class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
