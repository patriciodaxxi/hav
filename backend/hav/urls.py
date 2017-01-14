from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from api.urls import api_urls
from incoming.views import debug

urlpatterns = [
    url(
        r'^$',
        TemplateView.as_view(template_name='hav/teaser.html')
    ),
    # API urls
    url(r'api/', include(api_urls, namespace='api')),
    url(r'admin/', debug),
    url(r'^dbadmin/', admin.site.urls),
    url(r'', include('cms.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
