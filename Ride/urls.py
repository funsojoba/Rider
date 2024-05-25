from rest_framework.routers import DefaultRouter

from .views import CustomerRideViewSet, DriverRideViewSet


router = DefaultRouter()

router.register(r"customer", CustomerRideViewSet, basename="customer-rides")
router.register(r"driver", DriverRideViewSet, basename="driver-rides")

urlpatterns = router.urls
