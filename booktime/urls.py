from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html")),
    path('', include('main.urls')), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Add this line to serve media files in development
