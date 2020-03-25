"""canvaslite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from . import views
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static


app_name = 'lms'
urlpatterns = [
    path('', views.home_view_public, name='home_view_public'),
    re_path(r'^home_view_public/$', views.home_view_public, name='home_view_public'),
    path('assignment_list', views.assignment_list, name='assignment_list'),
    path('assignment/create/', views.assignment_new, name='assignment_new'),
    path('assignment/<int:pk>/edit/', views.assignment_edit, name='assignment_edit'),
    path('assignment/<int:pk>/delete/', views.assignment_delete, name='assignment_delete'),
    path('course_list', views.course_list, name='course_list'),
    path('course/create/', views.course_new, name='course_new'),
    path('course/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('course/<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('announcement_list', views.announcement_list, name='announcement_list'),
    path('announcement_view_public', views.announcement_view_public, name='announcement_view_public'),
    path('announcement_view_instructor', views.announcement_view_instructor, name='announcement_view_instructor'),
    path('announcement/create/', views.announcement_create_instructor, name='announcement_create_instructor'),
    path('announcement/<int:pk>/edit/', views.announcement_edit_instructor, name='announcement_edit_instructor'),
    path('announcement/<int:pk>/delete/', views.announcement_delete_instructor, name='announcement_delete_instructor'),
    path('file/upload/', views.model_form_upload, name="model_form_upload"),
    path('file_list', views.file_list, name="file_list"),
    path('file/<int:pk>/delete/', views.delete_file, name="delete_file"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
