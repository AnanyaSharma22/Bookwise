"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from catalog.views.web import HomeView

admin.site.site_header = 'BookWise Admin Panel'
admin.site.site_title = 'BookWise Admin Panel'

urlpatterns = [
    url(r'^admin-portal/',admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # url(r'', include('accounts.weburls', namespace='account')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^account/', include('accounts.weburls', namespace='account')),
    url(r'', include('catalog.weburls', namespace='catalog')),
    url(r'^catalog/', include('catalog.apiurls', namespace='catalogapi')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    # url(r'^oauth/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)