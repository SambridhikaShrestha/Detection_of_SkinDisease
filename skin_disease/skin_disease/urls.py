from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from main import views as main_views
from users import views as users_views
from rest_framework.authtoken import views as auth_views
from users.views import UserSerializer
from rest_framework.authtoken import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("detection/", main_views.index, name="index"),
    path('login/', users_views.LoginPage, name='login'),
    path('signup/', users_views.SignupPage, name='signup'),
    path('user/', users_views.HomePage, name='home'),
    path('logout/', users_views.LogoutPage, name='logout'),
    path("", users_views.userhome, name="userhome"),
    path('api-token-auth/', views.obtain_auth_token), 
    path('register/', users_views.RegisterUser.as_view(), name='register'), 

]


if settings.DEBUG:
    # setting this to view media files from admin panel
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)