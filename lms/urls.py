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
app_name = 'lms'
urlpatterns = [
    path('assignment_list', views.assignment_list, name='assignment_list'),
    path('assignment/create/', views.assignment_new, name='assignment_new'),
    path('assignment/<int:pk>/edit/', views.assignment_edit, name='assignment_edit'),
    path('assignment/<int:pk>/delete/', views.assignment_delete, name='assignment_delete'),
]
