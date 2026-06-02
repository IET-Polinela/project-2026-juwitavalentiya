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