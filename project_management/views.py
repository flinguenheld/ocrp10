from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from project_management.permissions import IsProjectContributor
from project_management.serializer import (ProjectSerializer,
                                            ContributorSerializer,
                                            ContributorAddSerializer)
from project_management.models import (Project,
                                        Contributor)


class ProjectViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]

    def list(self, request):
        # IsAuthenticated only

        contribs = Contributor.objects.filter(user=request.user)  # A CONFIRMER !!!!!!!!!!
        queryset = Project.objects.filter(contributor__in=contribs)

        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # IsAuthenticated only

        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            new_contributor = Contributor(user=request.user,
                                          project=Project.objects.first(),
                                          permission=Contributor.Permission.CREATOR)
            new_contributor.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):

        # Creator only
        project = get_object_or_404(Project, pk=pk)
        self.check_object_permissions(request=request, obj=project)

        contributors = Contributor.objects.filter(project=project)

        for c in contributors:
            c.delete()

        project.delete()

        return Response(data='Supprimé', status=status.HTTP_204_NO_CONTENT)


# class ProjectUserViewSet(ViewSet):
class ProjectUserViewSet(viewsets.GenericViewSet):

    queryset = Contributor.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]

    def list(self, request, project_pk):

        # Contributor only
        self.check_object_permissions(request, obj=get_object_or_404(Project, pk=project_pk))

        contribs = Contributor.objects.filter(project=project_pk)
        serializer = ContributorSerializer(contribs, many=True)

        return Response(serializer.data)

    def create(self, request, project_pk):

        # Creator only
        self.check_object_permissions(request, obj=get_object_or_404(Project, pk=project_pk))

        serializer = ContributorAddSerializer(data={'project': project_pk,
                                                  'user': request.data['new_contributor'],
                                                  'permission': Contributor.Permission.CONTRIBUTOR})

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, project_pk=None):

        # Creator only
        self.check_object_permissions(request, obj=get_object_or_404(Project, pk=project_pk))

        contributor = Contributor.objects.filter(user=pk, project=project_pk)

        if contributor:
            if contributor.first().permission != Contributor.Permission.CREATOR:
                contributor.first().delete()
                return Response(data='Supprimé', status=status.HTTP_204_NO_CONTENT)

            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
