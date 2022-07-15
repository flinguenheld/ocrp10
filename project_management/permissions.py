from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from project_management.models import (Project,
                                       Contributor,
                                       Issue)


class IsProjectContributor(permissions.BasePermission):

    def has_permission(self, request, view):

        print('LE CONTRIBUTEUR !!!!!!!!')  #−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−− 
        project = get_object_or_404(Project, pk=view.kwargs['project_pk'])
        if Contributor.objects.filter(user=request.user, project=project):
            return True

        raise PermissionDenied("Only project's contributors are authorized to do this action")


class IsProjectCreator(permissions.BasePermission):

    def has_permission(self, request, view):

        print('LE CREATEUR !!!')  #−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−− 
        if 'project_pk' in view.kwargs:
            project = get_object_or_404(Project, pk=view.kwargs['project_pk'])
        else:
            project = get_object_or_404(Project, pk=view.kwargs['pk'])

        contributor = Contributor.objects.filter(user=request.user, project=project).last()
        if contributor and contributor.permission == Contributor.Permission.CREATOR: 
            return True

        raise PermissionDenied("Only the project's creator is authorized to do this action")


class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        print('L AUTEUR !!!!!')  #−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−− 
        if request.user == obj.author:
            return True

        raise PermissionDenied("Only the author is authorized to do this action")


class IsIssueInProject(permissions.BasePermission):
    """ Used to check the url
        If the issue is really a part of the project """

    def has_permission(self, request, view):
        if 'project_pk' in view.kwargs and 'issue_pk' in view.kwargs:
            issue = get_object_or_404(Issue, pk=view.kwargs['issue_pk'])
            if str(issue.project_id) == view.kwargs['project_pk']:
                return True
            else:
                raise PermissionDenied(f"The issue {view.kwargs['issue_pk']} "
                                       f"has no link with the project {view.kwargs['project_pk']}")

        return False
