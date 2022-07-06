from django.urls import path, include
from rest_framework import routers

from project_management import views


router = routers.SimpleRouter()
router.register('project', views.ProjectViewSet, basename='project')


prout = views.ProjectViewSet.as_view({
                                         # 'get': 'list',
                                         'put': 'update'
                                     })



urlpatterns = [
    path('api/', include(router.urls)),
    path('prout/', prout, name='prout')
]
