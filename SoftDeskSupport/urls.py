from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from authentication.views import signup
from SoftDeskApp.views import (project_creation_view,
                               issue_creation_view,
                               comment_creation_view,
                               homepage,
                               ProjectViewSet,
                               IssueViewSet,
                               CommentViewSet,
                               AdminProjectViewSet,
                               )

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = routers.SimpleRouter()

router.register('project', ProjectViewSet, basename='project')
router.register('issue', IssueViewSet, basename='issue')
router.register('comment', CommentViewSet, basename='comment')
router.register('admin/project', AdminProjectViewSet, basename='admin-project')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('home/', homepage, name='home'),
    path('project_creation/', project_creation_view, name='project_creation'),
    path('issue_creation/', issue_creation_view, name='issue_creation'),
    path('comment_creation/', comment_creation_view, name='comment_creation'),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
]
