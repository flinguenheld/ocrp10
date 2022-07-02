from django.urls import path, include
from rest_framework import routers

from project_management import views


router = routers.SimpleRouter()
router.register('project', views.ProjectViewSet, basename='project')

urlpatterns = [
    path('api/', include(router.urls)),
]
