from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", accounts_views.login_views, name="home"),
    path("", include("django.contrib.auth.urls")),
    path("tu_talk/", include("tu_talk.urls")),
    path("tu_party/", include("tu_party.urls")),
    path("user/", include(("user_edit.urls"))),
    path("tu_alert/", include("tu_alert.urls")),
    path('tu_review/', include(('tu_review.urls'))),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
