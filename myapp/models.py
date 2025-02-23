from django.db import models

class Category(models.Model): # ★ Category モデルを作成
    name = models.CharField('カテゴリ名', max_length=20) # ★ カテゴリ名フィールド

    def __str__(self):
        return self.name

class Diary(models.Model):
    title = models.CharField(max_length=200, verbose_name='タイトル')
    content = models.TextField(verbose_name='本文')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    is_important = models.BooleanField(default=False, verbose_name='重要') # ★ is_important フィールドを追加
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='カテゴリ') # 外部キーを追加

    def __str__(self):
        return self.title