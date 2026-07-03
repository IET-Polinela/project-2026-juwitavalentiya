from rest_framework.routers import DefaultRouter
from .api_views import ReportViewSet

router = DefaultRouter()

# Path tunggal /api/report/ sesuai matriks pengujian resmi lab.
router.register(r'report', ReportViewSet)

urlpatterns = router.urls