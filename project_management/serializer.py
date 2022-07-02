from rest_framework.serializers import ModelSerializer

from project_management.models import Project


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type']

