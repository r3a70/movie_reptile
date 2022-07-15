from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import main, specify_movie, add_movie, add_tag, add_country, add_actor, add_link, delete_movie, home,\
    delete_tag, delete_country, delete_actor, delete_link


urlpatterns = [
    path('', home),
    path('api/v1/', main),
    path('api/v1/<int:movie>/', specify_movie),
    path('api/v1/movie/', add_movie),
    path('api/v1/movie/delete/<int:movie>/', delete_movie),
    path('api/v1/tag/', add_tag),
    path('api/v1/tag/delete/<int:tag>/', delete_tag),
    path('api/v1/country/', add_country),
    path('api/v1/country/delete/<int:country>/', delete_country),
    path('api/v1/actor/', add_actor),
    path('api/v1/actor/delete/<int:actor>/', delete_actor),
    path('api/v1/link/', add_link),
    path('api/v1/link/delete/<int:link>/', delete_link),
    path('auth/', include('rest_framework.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
