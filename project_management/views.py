from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from project_management.permissions import IsCreator
from project_management.serializer import ProjectSerializer
from project_management.models import (Project,
                                        Contributor)




class ProjectViewSet(ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsCreator]
    # permission_classes = [IsProjectCreator]


    def list(self, request):

        print(request.user)
        contribs = Contributor.objects.filter(user=request.user)  # A CONFIRMER !!!!!!!!!!
        queryset = Project.objects.filter(contributor__in=contribs)

        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):

        # serializer = ProjectSerializer(data=request.data)
        serializer = ProjectSerializer(
            context={'request': request}, data=request.data)

        if serializer.is_valid():
            serializer.save()

            new_contributor = Contributor(user=request.user,
                                          project=Project.objects.last(),
                                          permission=Contributor.Role.CREATOR)
            new_contributor.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):

        project = Project.objects.get(pk=pk)
        contributors = Contributor.objects.filter(project=project)

        for c in contributors:
            c.delete()

        project.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
