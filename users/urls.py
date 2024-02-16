from django.urls import path

from blog import settings
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static



urlpatterns = [
    path('register/', views.RegisterViewSet.as_view(), name='register'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    # password reset urls by convention

    path('password-reset/', views.MyPasswordResetView.as_view(), name='password_reset'),

    path('password-reset/done',
          auth_views.PasswordResetView.as_view(template_name='users/password_reset_done.html'), 
          name='password_reset_done'),

     path('password-reset-confirm/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
          name='password_reset_confirm'),

    path('password-reset-complete',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
        name='password_reset_complete'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)