from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

router = routers.SimpleRouter()
# router.register('user', views.UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('signup/', views.SignUpView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
