from django.contrib import admin
from project_management import models

admin.site.register(models.Project)
admin.site.register(models.Contributor)
admin.site.register(models.Issue)
admin.site.register(models.Comment)
