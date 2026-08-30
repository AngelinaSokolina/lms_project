from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# Импорты для документации
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка документации
schema_view = get_schema_view(
    openapi.Info(
        title="LMS API Documentation",
        default_version='v1',
        description="Документация для API LMS-системы",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT-эндпоинты
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Документация (доступна всем)
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # API приложений
    path('api/', include('lms.urls')),
    path('api/', include('users.urls')),
    path('api/', include('habits.urls')),
]

# Для отображения медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)