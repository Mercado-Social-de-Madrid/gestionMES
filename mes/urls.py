"""vicci URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from core import urls as core_urls
from simple_bpm import urls as bpm_urls

urlpatterns = [
    url(r'^', include(core_urls)),
    url(r'^bpm/', include(bpm_urls, namespace='bpm')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^management/', include('management.urls', namespace='management')),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^payments/', include('payments.urls')),
    url(r'^pay/', include('sermepa.urls')),
    url(r'^admin/', admin.site.urls),
] + \
  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


