"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin

from api.urls import get_api

urlpatterns = [
    path('', include('core.urls')),
    path('', include('currency.urls', namespace='currency')),
    path('bpm/', include('simple_bpm.urls', namespace='bpm')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('management/', include('management.urls', namespace='management')),
    #path('jet/', include('jet.urls', 'jet')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('intercoop/', include('intercoop.urls', namespace='intercoop')),
    path('', include('social_balance.urls', namespace='balance')),
    path('pay/', include('sermepa.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(get_api('v1').urls)),

]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

