from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from project_management.permissions import (ProjectViewPermissions)

from project_management.serializer import (ProjectSerializer,
                                            ContributorSerializer,
                                            ContributorAddSerializer,
                                            IssueAddSerializer)
from project_management.models import (Project,
                                        Contributor,
                                        Issue)


class ProjectViewSet(mixins.RetrieveModelMixin,  # Creator only
                     mixins.UpdateModelMixin,    # Creator only
                     viewsets.GenericViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectViewPermissions]

    def list(self, request):
        # IsAuthenticated only

        contribs = Contributor.objects.filter(user=request.user)
        queryset = Project.objects.filter(contributor__in=contribs)

        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # IsAuthenticated only

        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            new_contributor = Contributor(user=request.user,
                                          project=Project.objects.last(),
                                          permission=Contributor.Permission.CREATOR)
            new_contributor.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):

        # Project's creator only
        project = get_object_or_404(Project, pk=pk)
        self.check_object_permissions(request=request, obj=project)

        # Also delete all project's contributors
        contributors = Contributor.objects.filter(project=project)
        for c in contributors:
            c.delete()

        project.delete()

        return Response(data='Supprimé', status=status.HTTP_204_NO_CONTENT)


class ProjectUserViewSet(viewsets.GenericViewSet):
    """ Views for /projects/<id>/users/"""

    queryset = Contributor.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectViewPermissions]

    def list(self, request, project_pk):

        # Contributor only
        self.check_object_permissions(request, obj=get_object_or_404(Project, pk=project_pk))

        contribs = Contributor.objects.filter(project=project_pk)
        serializer = ContributorSerializer(contribs, many=True)

        return Response(serializer.data)

    def create(self, request, project_pk):

        # Project's creator only
        self.check_object_permissions(request, obj=get_object_or_404(Project, pk=project_pk))

        data = {'project': project_pk, 'permission': Contributor.Permission.CONTRIBUTOR}

        if 'new_contributor' in request.data:
            data['user'] = request.data['new_contributor']

        serializer = ContributorAddSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, project_pk=None):

        # Project's creator only
        self.check_object_permissions(request, obj=get_object_or_404(Project, pk=project_pk))

        contributor = Contributor.objects.filter(user=pk, project=project_pk)

        if contributor:
            if contributor.last().permission != Contributor.Permission.CREATOR:
                contributor.last().delete()
                return Response(data='Supprimé', status=status.HTTP_204_NO_CONTENT)

            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class IssueViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):

    queryset = Issue.objects.all()
    serializer_class = IssueAddSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, project_pk=None):

        project = get_object_or_404(Project, pk=project_pk)

        serializer = IssueAddSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(project=project, creator=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
