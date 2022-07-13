from rest_framework import permissions

from project_management.models import Contributor


class ProjectViewPermissions(permissions.BasePermission):
    """ Permissions for ProjectViewSet and ProjectUserViewSet
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
