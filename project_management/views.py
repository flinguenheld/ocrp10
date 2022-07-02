from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from project_management.serializer import ProjectSerializer
from project_management.models import Project


class ProjectViewSet(ModelViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        
        queryset = Project.objects.all()
        return queryset
