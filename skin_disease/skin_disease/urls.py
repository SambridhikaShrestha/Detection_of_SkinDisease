from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from main import views as main_views
from users import views as users_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("detection/", main_views.index, name="index"),
    path('login/', users_views.LoginPage, name='login'),
    path('signup/', users_views.SignupPage, name='signup'),
    path('user/', users_views.HomePage, name='home'),
    path('logout/', users_views.LogoutPage, name='logout'),
    path("", users_views.userhome, name="userhome"),
]


if settings.DEBUG:
    # setting this to view media files from admin panel
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)