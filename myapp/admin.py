from django.contrib import admin
from .models import Diary, Category

def make_important(modeladmin, request, queryset):  # ★ カスタムアクション関数を定義
    rows_updated = queryset.update(is_important=True)  # 選択された日記を「重要」にする
    if rows_updated == 1:
        message_bit = "1件の日記を"
    else:
        message_bit = f"{rows_updated}件の日記を"
    modeladmin.message_user(request, f"{message_bit}重要にしました。", level='SUCCESS')  # ユーザーにメッセージを表示
make_important.short_description = "選択した日記を重要にする"  # ★ アクションの説明文を設定

class DiaryAdmin(admin.ModelAdmin):  # ★ DiaryAdmin クラスを定義
    list_display = ('title', 'created_at', 'category', 'is_important')  # ★ カテゴリを追加
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'is_important', 'category')  # ★ カテゴリでのフィルタリングを追加
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (  # ★ fieldsets にカテゴリを追加
        ('基本情報', {
            'classes': ('collapse',),
            'fields': ('title', 'created_at', 'category'),
        }),
        ('内容', {
            'fields': ('content',),
        }),
    )
    actions = [make_important]

admin.site.register(Category)  # ★ Category モデルを管理画面に登録
admin.site.register(Diary, DiaryAdmin)  # ★ DiaryAdmin クラスと紐付けて登録