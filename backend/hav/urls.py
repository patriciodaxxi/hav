from django.conf.urls import url, include
from django.contrib import admin as django_admin
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test

from api.urls import api_urls

hav_admin_patterns = ([
    url(
        r'',
        user_passes_test(lambda u: u.is_superuser)(TemplateView.as_view(template_name='administration/index.html')),
        name='root'
    )],
    'hav_admin'
)

urlpatterns = [
    url(
        r'^$',
        TemplateView.as_view(template_name='hav/teaser.html')
    ),
    # API urls
    url(r'^api/', include(
        (api_urls, 'api'),
        namespace='api')
    ),
    url(r'^admin/', include(hav_admin_patterns, namespace='hav_admin')),
    url(r'^dbadmin/', django_admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
