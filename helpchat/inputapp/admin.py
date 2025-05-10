# inputapp/admin.py
from django.contrib import admin
from .models import Inquiry, Profile

admin.site.register(Inquiry)  # Inquiry モデルを管理画面に登録
admin.site.register(Profile)