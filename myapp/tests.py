
from django.test import TestCase, Client
from django.urls import reverse
from .models import Diary, Category
from .forms import DiaryForm

class DiaryFormTests(TestCase): # TestCase を継承したテストクラス

    def test_valid_form(self): # テストケース (正常なフォーム)
        test_category = Category.objects.create(name='仕事')
        form_data = {
            'title': 'テストタイトル',
            'content': 'テストコンテンツ',
            'category': test_category.id # カテゴリID (既存のカテゴリを想定)
        }
        form = DiaryForm(data=form_data) # フォームにデータを渡す
        self.assertTrue(form.is_valid()) # is_valid() が True であることを検証 (バリデーション成功)

    def test_invalid_form_no_title(self): # テストケース (タイトルなしの異常なフォーム)
        test_category = Category.objects.create(name='仕事')
        form_data = {
            'content': 'テストコンテンツ',
            'category': test_category.id
        }
        form = DiaryForm(data=form_data)
        self.assertFalse(form.is_valid()) # is_valid() が False であることを検証 (バリデーション失敗)
        self.assertIn('title', form.errors) # form.errors に 'title' エラーが含まれていることを検証

class DiaryListViewTests(TestCase): # TestCase を継承したテストクラス

    def setUp(self): # テスト実行前の準備処理 (setUp メソッド)
        self.client = Client() # テストクライアントを作成
        self.category = Category.objects.create(name='仕事') # テスト用カテゴリを作成
        Diary.objects.create(title='日記1', content='日記1の本文', category=self.category) # テスト用日記データを作成
        Diary.objects.create(title='日記2', content='日記2の本文', category=self.category)

    def test_diary_list_view(self): # テストケース (日記一覧ページへのGETリクエスト)
        response = self.client.get(reverse('diary_list')) # diary_list ビューへ GET リクエストを送信
        self.assertEqual(response.status_code, 200) # HTTPステータスコードが 200 であることを検証 (正常レスポンス)
        self.assertTemplateUsed(response, 'myapp/diary_list.html') # 'myapp/diary_list.html' テンプレートが使用されていることを検証
        self.assertEqual(len(response.context['diaries']), 2) # コンテキスト変数 'diaries' の要素数が 2 であることを検証 (日記データが2件取得されていること)
        self.assertContains(response, '日記1') # レスポンス内容に '日記1' という文字列が含まれていることを検証
        self.assertContains(response, '日記2')

    def test_diary_list_view_no_diaries(self): # テストケース (日記データが存在しない場合)
        Diary.objects.all().delete() # 全ての日記データを削除
        response = self.client.get(reverse('diary_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/diary_list.html')
        self.assertEqual(len(response.context['diaries']), 0) # コンテキスト変数 'diaries' の要素数が 0 であることを検証 (日記データが0件であること)
        self.assertNotContains(response, '日記1') # レスポンス内容に '日記1' という文字列が含まれていないことを検証