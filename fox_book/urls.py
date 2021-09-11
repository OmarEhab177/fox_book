"""fox_book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_auth.views import PasswordResetConfirmView
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from fox_book import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("test/api/v1/", include("core.urls")),
    path('accounts/', include('allauth.urls')),

    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # fcm device
    path('create/device', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
    
]

# apps url
urlpatterns += [
    path("api/v1/", include("core.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# dashboard
urlpatterns += [
    # Menu    
    path('',views.DashboardView.as_view(),name='dashboard'),# Dashboard
    path('menu/calendar',views.CalendarView.as_view(),name='calendar'),# Calender
    path('menu/chat',views.ChatView.as_view(),name='chat'),# Chat
    path('menu/app-kanban-board',views.KanbanBoardView.as_view(),name='app-kanban-board'),# Kanban Board
   
    # Apps 
    path('ecommerce/',include('ecommerce.urls')),# Ecommerce
    path('email/',include('mail.urls')),# Email
    path('layouts/',include('layouts.urls')),# Layout
    path('pages/',include('utility.urls')),# Utility
    path('components/',include('components.urls')),# Components
    path('authentication/',include('authentication.urls')),# Authentication
    
    # path('admin/', admin.site.urls),# Admin
]

if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

router = DefaultRouter()
router.register('devices', FCMDeviceAuthorizedViewSet)

urlpatterns += [
    path('devices/', include(router.urls)),
]

LOGIN_URL = "authentication/login"