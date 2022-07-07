from rest_framework import serializers

from rest_framework.validators import UniqueTogetherValidator

from authentication.models import User
from authentication.serializer import SignUpSerializer

from project_management.models import (Project,
                                        Contributor,
                                        Issue)


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'time_created']


class ContributorAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['project', 'user', 'permission']

        validators = [
            UniqueTogetherValidator(
                queryset=Contributor.objects.all(),
                fields=['project', 'user']
            )
        ]


class ContributorSerializer(serializers.ModelSerializer):

    user = SignUpSerializer()

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'permission']


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'project', 'creator',
            'assigned_to', 'priority', 'status', 'tag' 'time_created']
