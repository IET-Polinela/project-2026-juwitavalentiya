from rest_framework.routers import DefaultRouter
from .api_views import ReportViewSet

router = DefaultRouter()

# UBAH report → reports (biar sesuai lab & konsisten)
router.register(r'reports', ReportViewSet)

urlpatterns = router.urls