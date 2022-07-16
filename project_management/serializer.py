from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from authentication.serializer import UserSerializer
from project_management.models import (Project,
                                        Contributor,
                                        Issue,
                                        Comment)


# ##################################################################
class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'time_created']


class ProjectSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'type']


class ProjectDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'time_created']


# ##################################################################
class ContributorAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user', 'project', 'permission']

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
        fields = ['user', 'permission']


# ##################################################################
class IssueSerializer(serializers.ModelSerializer):

    author = UserSerializer()
    assigned = UserSerializer()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'author', 'assigned',
                  'priority', 'status', 'tag', 'time_created']


class IssueSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title']


class IssueAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'assigned', 'priority', 'status', 'tag']


# ##################################################################
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description']


class CommentDetailsSerializer(serializers.ModelSerializer):

    issue = IssueSimpleSerializer()
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue', 'author', 'time_created']


class CommentAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description']
