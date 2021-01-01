from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_completed.html'), name='password_reset_complete'),
    path('image_upload/', views.image_upload, name='image_upload'),
    path('image_upload/predict', views.predict, name='predict'),
    path('view_profile', views.view_profile, name='view_profile'),
    path('about/', views.about, name='about'),
    path('system/', views.system, name='system'),
    path('doctors/', views.doctors, name='doctors'),
    path('skincancer/', views.skincancer, name='skincancer'),
    path('cancertypes/', views.cancertypes, name='cancertypes'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


