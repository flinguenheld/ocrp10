from rest_framework import permissions

from project_management.models import Contributor



class IsProjectContributor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if Contributor.objects.filter(user=request.user, project=obj):
            return True

        return False

class IsProjectCreator(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):


        print('LE CREATEUR !!!')
        contributor = Contributor.objects.filter(user=request.user, project=obj).last()
        if contributor and contributor.permission == Contributor.Permission.CREATOR: 
            return True

        return False

class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user == obj.author:
            return True

        return False


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


class IssueCommentViewPermissions(permissions.BasePermission):
    """ Permissions for IssueViewSet and CommandViewSet. """

    def has_object_permission(self, request, view, obj):

        if request.method == 'GET' or request.method == 'POST':
            # obj -> Project
            if Contributor.objects.filter(user=request.user, project=obj):
                return True

        elif request.method == 'PUT' or request.method == 'DELETE':
            # obj -> Issue or Comment
            if request.user == obj.author:
                return True

        return False
