from rest_framework.routers import DefaultRouter

from .views import DriverViewSet


routers = DefaultRouter()

routers.register(prefix="", viewset=DriverViewSet, basename="driver")

urlpatterns = routers.urls
