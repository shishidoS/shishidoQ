# helpchat/urls.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from inputapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('input/', views.input_view, name='input_view'),
    path('result/', views.result_view, name='result_view'),
    path('', lambda request: redirect('input_view')),
]
