from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter


from project_management import views


router = routers.SimpleRouter()
router.register(r'project', views.ProjectViewSet, basename='project')

project_user = NestedSimpleRouter(router, r'project', lookup='project')
project_user.register(r'users', views.ProjectUserViewSet, basename='project_user')


prout = views.ProjectViewSet.as_view({
                                         # 'get': 'list',
                                         'put': 'update'
                                     })



urlpatterns = [
    path('', include(router.urls)),
    path('', include(project_user.urls)),
    path('prout/', prout, name='prout')
]
