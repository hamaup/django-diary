from rest_framework import serializers
from .models import Diary, Category

class CategorySerializer(serializers.ModelSerializer): # Category モデル用シリアライザー
    class Meta:
        model = Category
        fields = ['id', 'name'] # API で出力するフィールド


class DiarySerializer(serializers.ModelSerializer): # Diary モデル用シリアライザー
    category = CategorySerializer(read_only=True) # CategorySerializer をネストして category フィールドを表現

    class Meta:
        model = Diary
        fields = ['id', 'title', 'content', 'category', 'created_at'] # API で出力するフィールド