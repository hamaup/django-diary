from django.urls import path, include
from . import views
from .views import DiaryListAPIView # ★ DiaryListAPIView をインポート

urlpatterns = [
    path('', views.diary_list, name='diary_list'),
    path('diary/', views.diary_list, name='diary_list'),
    path('diary/create/', views.diary_create, name='diary_create'),
    path('diary/<int:diary_id>/', views.diary_detail, name='diary_detail'),
    path('diary/<int:diary_id>/edit/', views.diary_edit, name='diary_edit'),
    path('diary/<int:diary_id>/delete/', views.diary_delete, name='diary_delete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/create/', views.user_create, name='user_create'), # ★ ユーザー登録ページの URL パターンを追加
    path('api/diary/', DiaryListAPIView.as_view(), name='diary_list_api'), # ★ API エンドポイントを追加
]