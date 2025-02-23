from django import forms
from .models import Diary, Category # ★ Category モデルをインポート
from django.contrib.auth.forms import UserCreationForm

class DiaryForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label="カテゴリを選択しない") # ★ カテゴリ選択フィールドを追加

    class Meta:
        model = Diary
        fields = ('title', 'content', 'category') # ★ fields に category を追加

class UserCreateForm(UserCreationForm):
    class Meta:
        model = UserCreationForm.Meta.model
        fields = ('username', 'email')