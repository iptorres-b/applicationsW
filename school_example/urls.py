from django.contrib import admin
from django.http import request
from django.urls import path
from users import views as users_views
# Static files config
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',users_views.login_view, name='login'),
    path('new/', users_views.signup, name='signup'),
    path('landing/', users_views.landing, name='landing'),
    path('logout/',users_views.logout_view, name='logout')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
