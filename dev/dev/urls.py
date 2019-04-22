from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
	path('home/', include('home.urls')),
	path('admin/', admin.site.urls),
	path('', RedirectView.as_view(url='/home/', permanent=True))
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)