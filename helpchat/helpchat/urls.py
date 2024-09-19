# helpchat/urls.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect  # 'redirect'は'django.urls'ではなく、'django.shortcuts'からインポート

from inputapp import views  # ビューのインポート

urlpatterns = [
    path('admin/', admin.site.urls),
    path('input/', views.input_view, name='input_view'),
    # ルートURLでリダイレクトを設定
    path('', lambda request: redirect('input_view')),  # '/'にアクセス時に 'input/'へリダイレクト
]
