
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from chat.services.consumers import ChatConsumer


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include("chat.controller.index")),
    path('api/schema/',SpectacularAPIView.as_view(),name="schema"),
    path("api/schema/docs",SpectacularSwaggerView.as_view(url_name = "schema")),
    re_path(r'ws/chat/room/(?P<id>\d+)/$',ChatConsumer.as_asgi())
    

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
