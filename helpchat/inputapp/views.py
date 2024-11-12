from django.shortcuts import render
from .forms import InputForm
from .models import Inquiry
from janome.tokenizer import Tokenizer
import google.generativeai as genai

# JanomeのTokenizerを初期化
t = Tokenizer(wakati=False)

# Google Gemini APIの設定
genai.configure(api_key='AIzaSyCmxISDqTCgH7ycqZTHDWjyqsL9Zf3qja0') 
gemini_model = genai.GenerativeModel('models/gemini-1.5-flash')

# 形態素解析と単語分割を行う関数
def word_split(word_text):
    return [token.reading for token in t.tokenize(word_text)]

# Geminiモデルへメッセージを送り、回答を取得する関数
def get_answer_from_gemini(message):
    response = gemini_model.generate_content(
        f'あなたはヘルプデスクサポートです。以下の問い合わせ内容に対し、テキスト表示で適切な解決策を提示してください。\n\n{message}'
    )
    return response.text

# Djangoのビュー関数
def input_view(request):
    if request.method == 'POST':
        form = InputForm(request.POST)

        if form.is_valid():
            company = form.cleaned_data['company']
            store = form.cleaned_data['store']
            staff = form.cleaned_data['staff']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Geminiへメッセージを送信し、AIの回答を取得
            gemini_message = f"会社: {company}\n店舗: {store}\n担当スタッフ: {staff}\n題名: {subject}\n内容: {message}\n"
            gemini_response = get_answer_from_gemini(gemini_message)

            # お問い合わせをデータベースに保存
            inquiry = Inquiry.objects.create(
                company=company,
                store=store,
                staff=staff,
                subject=subject,
                message=message,
                response=gemini_response
            )

            # 結果ページにリダイレクト
            return render(request, 'result.html', {'gemini_response': gemini_response})

    else:
        form = InputForm()

    # 過去のお問い合わせを取得
    inquiries = Inquiry.objects.order_by('-created_at')

    return render(request, 'input.html', {'form': form, 'inquiries': inquiries})
