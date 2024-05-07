from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from authentication.views import signup
from SoftDeskApp.views import (ProjectViewSet,
                               IssueViewSet,
                               CommentViewSet,
                               StaffIssueViewSet,
                               UserListViewSet,
                               ContributorViewSet
                               )

from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            TokenVerifyView
                                            )

router = routers.SimpleRouter()

router.register('project', ProjectViewSet, basename='project')
router.register('issue', IssueViewSet, basename='issue')
router.register('comment', CommentViewSet, basename='comment')
router.register('staff/issue', StaffIssueViewSet, basename='staff-issue')
router.register('user', UserListViewSet, basename='user')
router.register('contributor', ContributorViewSet, basename='contributor')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
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
