from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers

from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from project_management.permissions import (ProjectViewPermissions,
                                            IssueCommentViewPermissions,
                                            IsProjectContributor,
                                            IsProjectCreator,
                                            IsAuthor)

from project_management.models import (Project,
                                        Contributor,
                                        Issue,
                                        Comment)
from project_management.serializer import (ProjectSerializer,
                                            ProjectSimpleSerializer,
                                            ProjectDetailsSerializer,
                                            ContributorSerializer,
                                            ContributorAddSerializer,
                                            IssueSerializer,
                                            IssueAddSerializer,
                                            CommentSerializer,
                                            CommentAddSerializer)


class ProjectViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'create':
            permission_classes = [IsAuthenticated]

        else:
            permission_classes = [IsAuthenticated, IsProjectCreator]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == 'list' or self.action == 'retrieve':
            contribs = Contributor.objects.filter(user=self.request.user)
            return Project.objects.filter(contributor__in=contribs)

        else:
            return Project.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectSimpleSerializer

        elif self.action == 'retrieve':
            return ProjectDetailsSerializer

        else:
            return ProjectSerializer

    def perform_create(self, serializer):
        serializer.save()

        new_contributor = Contributor(user=self.request.user,
                                      project=Project.objects.last(),
                                      permission=Contributor.Permission.CREATOR)
        new_contributor.save()

    def perform_destroy(self, instance):

        # Also delete all project's contributors
        contributors = Contributor.objects.filter(project=instance)
        for c in contributors:
            c.delete()

        # Issues too ?? −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
        instance.delete()


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

        # Project's author only
        self.check_object_permissions(request, obj=get_object_or_404(Project, pk=project_pk))

        data = {'project': project_pk, 'permission': Contributor.Permission.CONTRIBUTOR}

        if 'new_contributor' in request.data:           # Serializer refused by validation if forgotten
            data['user'] = request.data['new_contributor']

        serializer = ContributorAddSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, project_pk=None):

        # Project's author only
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


class IssueViewSet(mixins.UpdateModelMixin,     # Issue's author only
                   mixins.DestroyModelMixin,    # Issue's author only
                   viewsets.GenericViewSet):

    queryset = Issue.objects.all()
    serializer_class = IssueAddSerializer
    permission_classes = [IsAuthenticated, IssueCommentViewPermissions]

    def list(self, request, project_pk):

        # Project contributors only
        project = get_object_or_404(Project, pk=project_pk)
        self.check_object_permissions(request, project)

        issues = Issue.objects.filter(project=project)
        serializer = IssueSerializer(issues, many=True)

        return Response(serializer.data)

    def create(self, request, project_pk=None):

        # Project contributors only
        project = get_object_or_404(Project, pk=project_pk)
        self.check_object_permissions(request, project)

        serializer = IssueAddSerializer(data=request.data)

        if serializer.is_valid():
            if Contributor.objects.filter(project=project, user=serializer.validated_data['assigned']):
                serializer.save(project=project, author=request.user)

            else:
                raise serializers.ValidationError("L'assigné doit être un contributeur du projet")

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(mixins.UpdateModelMixin,       # Comment's author only
                     mixins.DestroyModelMixin,      # Comment's author only
                     viewsets.GenericViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentAddSerializer
    permission_classes = [IsAuthenticated, IssueCommentViewPermissions]

    def list(self, request, project_pk=None, issue_pk=None):
        
        # Project contributors only
        self.check_object_permissions(request, get_object_or_404(Project, pk=project_pk))

        comments = Comment.objects.filter(issue=issue_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk=None, issue_pk=None):

        # Project contributors only
        self.check_object_permissions(request, get_object_or_404(Project, pk=project_pk))

        issue = get_object_or_404(Issue, pk=issue_pk)
        serializer = CommentAddSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(issue=issue, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, project_pk=None, issue_pk=None, pk=None):

        # Project contributors only
        self.check_object_permissions(request, get_object_or_404(Project, pk=project_pk))

        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
