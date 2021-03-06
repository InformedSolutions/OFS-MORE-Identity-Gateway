"""identity_gateway URL Configuration

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
import re

from django.conf import settings
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view

from application import views

schema_view = get_swagger_view(title='OFS-MORE Identity Service')

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'api/v1/user', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^api/v1/summary/(?P<name>\w+)/(?P<application_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
        views.summary_table, name="Summary"),
    url(r'^schema/$', schema_view),
    url(r'^', include(router.urls))
]

if settings.URL_PREFIX:
    prefixed_url_pattern = []
    for pat in urlpatterns:
        pat.regex = re.compile(r"^%s/%s" % (settings.URL_PREFIX[1:], pat.regex.pattern[1:]))
        prefixed_url_pattern.append(pat)
    urlpatterns = prefixed_url_pattern
