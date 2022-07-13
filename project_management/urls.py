from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from project_management import views


router = routers.SimpleRouter()
router.register(r'projects', views.ProjectViewSet, basename='projects')

project_user = NestedSimpleRouter(router, r'projects', lookup='project')
project_user.register(r'users', views.ProjectUserViewSet, basename='projects_user')

project_issue = NestedSimpleRouter(router, r'projects', lookup='project')
project_issue.register(r'issues', views.IssueViewSet, basename='projects_issue')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(project_user.urls)),
    path('', include(project_issue.urls)),
]
