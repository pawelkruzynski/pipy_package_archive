from django.urls import path

import webapps.package.views as webapps_views
from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from webapps.package import viewsets as package_viewset

router = DefaultRouter()
router.register(
    r'package', package_viewset.PackageViewset, basename='packagedocument'
)

urlpatterns = [
    path('', webapps_views.index, name='index'),
    path('api/v1/', include(router.urls)),
]
