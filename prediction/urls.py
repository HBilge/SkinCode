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


