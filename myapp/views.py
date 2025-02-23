from django.shortcuts import render, redirect, get_object_or_404
from .models import Diary
from .forms import DiaryForm, UserCreateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q # ★ Qオブジェクトをインポート

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DiarySerializer

class DiaryListAPIView(APIView): # APIView を継承した API ビュー
    def get(self, request, *args, **kwargs): # GET リクエスト処理
        diaries = Diary.objects.all() # 全ての日記データを取得
        serializer = DiarySerializer(diaries, many=True) # 複数データ (many=True) をシリアライズ
        return Response(serializer.data, status=status.HTTP_200_OK) # シリアライズしたデータを JSON レスポンスとして返す


def diary_list(request):
    diaries = Diary.objects.all().order_by('-created_at')
    search_query = request.GET.get('search_query') # ★ 検索キーワードを取得

    if search_query: # ★ 検索キーワードが入力されている場合
        diaries = diaries.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query) # ★ タイトルと内容で検索
        )

    return render(request, 'myapp/diary_list.html', {'diaries': diaries})

def diary_detail(request, diary_id):
    diary = get_object_or_404(Diary, pk=diary_id)
    return render(request, 'myapp/diary_detail.html', {'diary': diary})

@login_required # ★ @login_required デコレータを追加 (日記作成ページ)
def diary_create(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('diary_list')
    else:
        form = DiaryForm()
    return render(request, 'myapp/diary_create.html', {'form': form})

@login_required # ★ @login_required デコレータを追加 (日記編集ページ)
def diary_edit(request, diary_id):
    diary = get_object_or_404(Diary, pk=diary_id)
    if request.method == 'POST':
        form = DiaryForm(request.POST, instance=diary)
        if form.is_valid():
            form.save()
            return redirect('diary_detail', diary_id=diary_id)
    else:
        form = DiaryForm(instance=diary)
    return render(request, 'myapp/diary_edit.html', {'form': form, 'diary': diary})

@login_required # ★ @login_required デコレータを追加 (日記削除ページ)
def diary_delete(request, diary_id):
    diary = get_object_or_404(Diary, pk=diary_id)
    if request.method == 'POST':
        diary.delete()
        return redirect('diary_list')
    return render(request, 'myapp/diary_delete_confirm.html', {'diary': diary})

def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('diary_list')
    else:
        form = UserCreateForm()
    return render(request, 'myapp/user_create.html', {'form': form})