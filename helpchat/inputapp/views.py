from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from .models import Profile, Inquiry
from .forms import InquiryForm
import google.generativeai as genai
import os
from janome.tokenizer import Tokenizer
import urllib.parse

# Gemini APIキー設定
os.environ["GOOGLE_API_KEY"] = "GeminiAPIキー載せて"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")


# 形態素解析（わかち書き）
def extract_keywords(text):
    tokenizer = Tokenizer()
    words = [token.base_form for token in tokenizer.tokenize(text) if token.base_form not in ['です', 'ます', 'で', 'を', 'が', 'は']]
    return words


# キーワードに応じたプロフィール抽出
def find_relevant_profile(keywords):
    queries = Q()
    for word in keywords:
        queries |= Q(name__icontains=word)
        queries |= Q(university__icontains=word)
        queries |= Q(faculty__icontains=word)
        queries |= Q(grade__icontains=word)
        queries |= Q(hometown__icontains=word)
        queries |= Q(programming_languages__icontains=word)
        queries |= Q(frameworks__icontains=word)
        queries |= Q(tools__icontains=word)
        queries |= Q(certifications__icontains=word)
        queries |= Q(experiences__icontains=word)
        queries |= Q(achievements__icontains=word)
        queries |= Q(strengths__icontains=word)
        queries |= Q(hobbies__icontains=word)
        queries |= Q(future_goals__icontains=word)
        queries |= Q(additional_info__icontains=word)
    return Profile.objects.filter(queries).first()


# Gemini API連携（関連情報だけ送信）
def get_answer_from_gemini(question, profile):
    if not profile:
        return "関連するプロフィール情報が見つかりませんでした。"

    info_text = ""
    keyword_map = {
        "名前": ("name", profile.name),
        "大学名": ("university", profile.university),
        "学部・学科": ("faculty", profile.faculty),
        "学年": ("grade", profile.grade),
        "出身地": ("hometown", profile.hometown),
        "使用可能なプログラミング言語": ("programming_languages", profile.programming_languages),
        "使用可能なフレームワーク・ライブラリ": ("frameworks", profile.frameworks),
        "使用可能なツール・サービス": ("tools", profile.tools),
        "取得資格・認定": ("certifications", profile.certifications),
        "開発・研究・活動経験": ("experiences", profile.experiences),
        "実績・成果": ("achievements", profile.achievements),
        "強み・スキル": ("strengths", profile.strengths),
        "趣味・興味": ("hobbies", profile.hobbies),
        "将来の目標・志望動機": ("future_goals", profile.future_goals),
        "その他補足情報": ("additional_info", profile.additional_info),
    }

    # 質問とマッチする情報を抽出
    for word, value in keyword_map.items():
        if value and word in question:
            info_text += f"{word}: {value}\n"

    # 複数の候補にマッチする場合の処理
    synonym_map = {
        "strengths": ["強み", "スキル", "長所", "特技", "得意分野"],
        "achievements": ["実績", "成果", "達成"],
        "hobbies": ["趣味", "興味", "好きなこと"],
        "future_goals": ["目標", "志望動機", "将来", "キャリア"],
    }

    for field_name, synonyms in synonym_map.items():
        if any(syn in question for syn in synonyms):
            value = getattr(profile, field_name, None)
            if value:
                jp_field = [k for k, (f, _) in keyword_map.items() if f == field_name][0]
                info_text += f"{jp_field}: {value}\n"
                break 

    # 情報がなければデフォルトの情報を表示
    if not info_text:
        info_text = f"名前: {profile.name}\n大学名: {profile.university}\n"

    # Gemini APIへのプロンプト作成
    prompt = (
    "以下はある人物のプロフィール情報と、想定される質問です。\n"
    "与えられた情報の中から回答可能な内容をもとに、採用担当者や関係者が魅力を感じるように、"
    "第三者視点でポジティブに紹介してください。\n"
    "紹介文は300文字以内で、丁寧かつわかりやすい文章でまとめてください。\n\n"
    f"【人物情報】\n{info_text}\n\n"
    f"【質問】\n{question}"
)

    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API エラー: {e}")
        return "エラーが発生しました。"


# 質問入力ビュー
def input_view(request):
    if request.method == "POST":
        form = InquiryForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            keywords = extract_keywords(message)
            profile = find_relevant_profile(keywords)
            gemini_response = get_answer_from_gemini(message, profile)

            Inquiry.objects.create(
                subject="自己質問",
                message=message,
                response=gemini_response,
                profile=profile
            )

            params = {
                "gemini_response": gemini_response,
                "split_words": ",".join(keywords)
            }
            url = reverse("result_view") + "?" + urllib.parse.urlencode(params)
            return HttpResponseRedirect(url)
    else:
        form = InquiryForm()

    inquiries = Inquiry.objects.order_by('-id')[:10]  # 最近10件表示

    return render(request, "input.html", {
        "form": form,
        "inquiries": inquiries
    })


# 結果表示ビュー
def result_view(request):
    gemini_response = request.GET.get("gemini_response", "")
    split_words = request.GET.get("split_words", "").split(",")
    return render(request, "result.html", {
        "gemini_response": gemini_response,
        "split_words": split_words
    })
