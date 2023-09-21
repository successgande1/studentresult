"""
URL configuration for studentresult project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from accounts.views import custom_page_not_found, custom_page_forbidden, custom_server_not_found
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from accounts import views as account_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('404/', custom_page_not_found, name='custom_404'),
    path('403/', custom_page_forbidden, name='custom_403'),
    path('500/', custom_server_not_found, name='custom_500'),
    path('', include('pages.urls')),
    path('', include('accounts.urls')),
    path('', include('results.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'studentresult.urls.custom_page_not_found'

handler403 = 'studentresult.urls.custom_page_forbidden'

handler500 = 'studentresult.urls.custom_server_not_found'
