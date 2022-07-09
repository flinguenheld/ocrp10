from rest_framework import permissions

from project_management.models import Contributor


class IsProjectContributor(permissions.BasePermission):
    # message = 'nononon !!!!!!'

    def has_object_permission(self, request, view, obj):

        contributor = Contributor.objects.filter(user=request.user, project=obj).first()

        if contributor:

            if request.method == 'GET':
                return True

            elif ((request.method == 'PUT' or request.method == 'DELETE')
                    and contributor.permission == Contributor.Permission.CREATOR):
                return True

        return False
