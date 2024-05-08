from django.contrib import admin
from django.urls import path, include
from .views import landing_page, home_page, about_page

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('home/', home_page, name='home_page'),
    path('about', about_page, name='about_page'),
    path('books/', include('books.urls')),
    path('users/', include('users.urls')),

    # APIs
    path('api/', include('api.urls')),

    # Django REST Framework login
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Django accounts
    path('accounts/', include('django.contrib.auth.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'goodreads.views.handler404'