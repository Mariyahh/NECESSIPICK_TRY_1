from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import HomePage, Register, Login, Logout, profile, update_profile_picture

urlpatterns = [
    path('', HomePage, name='auth_home'),
    path('register/', Register, name='register-page'),
    path('login/', Login, name='login-page'),
    path('logout/', Logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/update_picture/', update_profile_picture, name='update-profile-picture'),  # Add this line
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)