"""StudyOnCurtainWall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import include, path, re_path
from django.views.static import serve

from Accounts.authChange import update_user_permissions
from Accounts.view2 import get_system_permissions
from Accounts.views import register, validate, user_login
from Accounts.returnEmail import get_current_user_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backend/', include('backend.urls')),
    path('register', register, name='register'),
    path('validate', validate, name='validate'),
    path('login', user_login, name='login'),
    path('show', get_system_permissions, name='get_system_permissions'),
    path('update-permissions', update_user_permissions, name='update-permissions'),
    path('get-info', get_current_user_info, name='get-current-user-email'),
    re_path(r'media/(?P<path>.*)', serve,{'document_root': settings.MEDIA_ROOT}),
]