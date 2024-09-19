from django.shortcuts import render
from .forms import InputForm
import os
from django.conf import settings
from janome.tokenizer import Tokenizer
import google.generativeai as genai

# JanomeのTokenizerを初期化
t = Tokenizer(wakati=False)

# Google Gemini APIの設定
genai.configure(api_key='AIzaSyCmxISDqTCgH7ycqZTHDWjyqsL9Zf3qja0')
gemini_model = genai.GenerativeModel('models/gemini-1.5-flash')

# ファイルを読み込む関数
def input_file(file_name, input_lines=False):
    file_path = os.path.join(settings.BASE_DIR, 'inputapp', 'search_word', file_name)
    with open(file_path, encoding='utf-8') as in_text:
        return in_text.readlines() if input_lines else in_text.read()

# 形態素解析と単語分割を行う関数
def word_split(word_text):
    return [token.reading for token in t.tokenize(word_text)]

# Geminiモデルへメッセージを送り、回答を取得する関数
def get_answer_from_gemini(message):
    response = gemini_model.generate_content(
        f'あなたはヘルプデスクの担当者です。\n以下の問い合わせ内容に対し、以下の事例と解決策をわかりやすい形で提示してください。'
        f'なお、問い合わせ者へ質問はできません。URLを追記することは禁止します。\n\n{message}'
    )
    return response.text

# 事例を検索し、マッチワード数でソートする関数
def find_similar_cases(input_words, jire_lines, answer_lines):
    results = [
        (jire_line.strip(), answer_lines[i].strip(),
         sum(word in word_split(jire_line.strip()) for word in input_words), i)
        for i, jire_line in enumerate(jire_lines)
    ]
    return sorted(results, key=lambda x: x[2], reverse=True)[:3]

# Geminiモデルへのメッセージを作成する関数
def build_gemini_message(input_text, similar_cases):
    message = f"問い合わせ内容：{input_text}\n"
    for i, (jire, answer, _, _) in enumerate(similar_cases):
        message += f"事例{i+1}：{jire}\n解決策：{answer}\n"
    return message

# Djangoのビュー関数
def input_view(request):
    if request.method == 'POST':
        form = InputForm(request.POST)

        if form.is_valid():
            input_user = form.cleaned_data['text_input']
            input_word = word_split(input_user)

            # 形態素解析で分割された単語を「、」で区切る
            split_words_display = "、".join(input_word)

            # 事例と回答ファイルを読み込む
            jire_lines = input_file('test_jire.txt', True)
            answer_lines = input_file('test_anser.txt', True)

            # 類似する事例を探す
            similar_cases = find_similar_cases(input_word, jire_lines, answer_lines)

            if similar_cases:
                # Geminiモデルに送信するメッセージを構築
                gemini_message = build_gemini_message(input_user, similar_cases)

                # Geminiから解決策を取得
                gemini_response = get_answer_from_gemini(gemini_message)
                search_result = f"Geminiからの回答:\n{gemini_response}"
            else:
                search_result = "該当する事例が見つかりませんでした。"

            # 分解された単語を表示
            result = f"ユーザーが入力した内容: {split_words_display}"
            return render(request, 'result.html', {'result': result, 'search_result': search_result})

    else:
        form = InputForm()

    return render(request, 'input.html', {'form': form})
