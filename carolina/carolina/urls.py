"""carolina URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from webpage import views
from django.conf.urls.i18n import i18n_patterns

from django.views.static import serve
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    
]

urlpatterns += i18n_patterns(
    path('', views.home, name='home'),
    path('',include('webpage.urls')),
)


admin.site.site_title = "Portal Carolina Administração"
admin.site.site_header = "Carolina"
admin.site.index_title = "Administração"
#admin.site.site_url = ''
admin.site.enable_nav_sidebar = True # Remove side bars from admin. 

