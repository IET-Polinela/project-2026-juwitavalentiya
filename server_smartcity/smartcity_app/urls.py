from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# REGISTER API
from usermanagement_24782014.api_views import RegisterView

# ========================================================
# ADDED FOR LAB 14: OPENAPI & DOCUMENTATION VIEWS
# ========================================================
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django_scalar.views import scalar_viewer


urlpatterns = [

    # =========================
    # ADMIN
    # =========================
    path('admin/', admin.site.urls),

    # =========================
    # WEB APPS (LAMA)
    # =========================
    path('', include('main_app.urls')),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    path('dashboard/', include('dashboard_24782014.urls')),

    # =========================
    # DRF API (REPORT)
    # =========================
    path('api/', include('main_app.api_urls')),

    # =========================
    # JWT AUTH
    # =========================
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # =========================
    # REGISTER USER (CITIZEN)
    # =========================
    path('api/register/', RegisterView.as_view(), name='register'),

    # ========================================================
    # ADDED FOR LAB 14: OPENAPI ENDPOINTS
    # ========================================================
    # 1. Endpoint untuk meng-generate file skema mentah (JSON/YAML)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # 2. Endpoint Swagger UI
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # 3. Endpoint Scalar UI
    path('api/docs/scalar/', scalar_viewer, name='scalar-ui'),

    # =========================
    # LOGIN WEB (HTML)
    # =========================
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout'
    ),
]