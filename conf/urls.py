from django.conf import settings
from django.urls import include, path

urlpatterns = [
    # vendor
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    # do not change
    path("core/", include("apps.core.urls")),
    # customize
    path("", include("apps.home.urls")),
    path(
        settings.CUSTOM_APP_URL.strip("/") + "/",
        include(f"{settings.CUSTOM_APP_NAME}.urls"),
    ),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
