
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from chat.services.accounts import register,login
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register',register,name = "register"),
    path('accounts/login',LoginView.as_view(template_name = "login.html"),name = "login"),
    path('accounts/profile/',include("chat.controller.chat_rooms")),
    path('',include("chat.controller.chat_rooms")),
    path('api/v1/',include("chat.controller.index")),
    path('api/schema/',SpectacularAPIView.as_view(),name="schema"),
    path("api/schema/docs",SpectacularSwaggerView.as_view(url_name = "schema")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
