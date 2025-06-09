from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("", include("apps.base.urls")),
    path("schools/", include("apps.schools.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    # from django.contrib import admin

    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        # path("dev-admin/", admin.site.urls),
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]