"""
URL configuration for SoftDeskSupport project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import authentication.views
import SoftDeskApp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', authentication.views.signup, name='signup'),
    path('home/', SoftDeskApp.views.homepage, name='home'),
    path('project_creation/', SoftDeskApp.views.project_creation_view, name='project_creation'),
    path('issue_creation/', SoftDeskApp.views.issue_creation_view, name='issue_creation'),
    path('comment_creation/', SoftDeskApp.views.comment_creation_view, name='comment_creation'),
]
