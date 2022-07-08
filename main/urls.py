from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import main, specify_movie


urlpatterns = [
    path('', main),
    path('<int:movie>/', specify_movie),
    path('auth/', include('rest_framework.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
