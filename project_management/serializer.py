from rest_framework import serializers

from project_management.models import (Project,
                                        Issue)


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'time_created']


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'project', 'creator',
            'assigned_to', 'priority', 'status', 'tag' 'time_created']
