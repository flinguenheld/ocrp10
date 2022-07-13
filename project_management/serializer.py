from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from authentication.serializer import UserSerializer
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
        read_only_fields = ['permission']

        validators = [
            UniqueTogetherValidator(
                queryset=Contributor.objects.all(),
                fields=['project', 'user']
            )
        ]


class ContributorSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'permission']


class IssueSerializer(serializers.ModelSerializer):

    creator = UserSerializer()
    assigned = UserSerializer()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'creator', 'assigned',
                  'priority', 'status', 'tag', 'time_created']


class IssueAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'assigned', 'priority', 'status', 'tag']
