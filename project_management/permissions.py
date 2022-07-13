from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from project_management.models import Contributor


class ProjectViewPermissions(permissions.BasePermission):
    """ Permissions for ProjectViewSet and ProjectUserViewSet.
        Their logics are equal:
            - Read : all contributors
            - Write : only the project's creator """

    def has_object_permission(self, request, view, obj):

        contributor = Contributor.objects.filter(user=request.user, project=obj).last()
        if contributor:

            if request.method == 'GET':
                return True

            elif ((request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE')
                    and contributor.permission == Contributor.Permission.CREATOR):
                return True

        return False

class IssueViewPermissions(permissions.BasePermission):
    """ Permissions for IssueViewSet. """

    def has_object_permission(self, request, view, obj):

        if request.method == 'GET' or request.method == 'POST':
            # obj -> Project
            if Contributor.objects.filter(user=request.user, project=obj):
                return True

        elif request.method == 'PUT' or request.method == 'DELETE':
            # obj -> Issue
            if request.user == obj.creator:
                return True

        return False
