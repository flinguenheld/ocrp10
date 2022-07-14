from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from project_management import views


router = routers.SimpleRouter()
router.register(r'projects', views.ProjectViewSet, basename='projects')
# /projects/{project_pk}/

project_router = NestedSimpleRouter(router, r'projects', lookup='project')
project_router.register(r'users', views.ProjectUserViewSet, basename='users')
# /projects/{project_pk}/users/{pk}/

project_router.register(r'issues', views.IssueViewSet, basename='issues')
# /projects/{project_pk}/issues/{pk}/

issue_router = NestedSimpleRouter(project_router, r'issues', lookup='issue')
issue_router.register(r'comments', views.CommentViewSet, basename='comments')
# /projects/{project_pk}/issues/{pk}/comments/{pk}/

urlpatterns = [
    path('', include(router.urls)),
    path('', include(project_router.urls)),
    path('', include(issue_router.urls)),
]
