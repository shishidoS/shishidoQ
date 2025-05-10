# inputapp/models.py
from django.db import models

class Profile(models.Model):
    name = models.CharField("名前", max_length=100)
    university = models.CharField("大学名", max_length=200, null=True, blank=True)
    faculty = models.CharField("学部・学科", max_length=200, null=True, blank=True)
    grade = models.CharField("学年", max_length=50, null=True, blank=True)
    hometown = models.CharField("出身地", max_length=100, null=True, blank=True)

    programming_languages = models.TextField("使用可能なプログラミング言語", blank=True, null=True)
    frameworks = models.TextField("使用可能なフレームワーク・ライブラリ", blank=True, null=True)
    tools = models.TextField("使用可能なツール・サービス", blank=True, null=True)
    certifications = models.TextField("取得資格・認定", blank=True, null=True)

    experiences = models.TextField("開発・研究・活動経験", blank=True, null=True)
    achievements = models.TextField("実績・成果", blank=True, null=True)
    strengths = models.TextField("強み・スキル", blank=True, null=True)
    hobbies = models.TextField("趣味・興味", blank=True, null=True)
    future_goals = models.TextField("将来の目標・志望動機", blank=True, null=True)
    additional_info = models.TextField("その他補足情報", blank=True, null=True)

    def __str__(self):
        return self.name

class Inquiry(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField("問い合わせ内容", max_length=255, null=True, blank=True)
    message = models.TextField("メッセージ", null=True, blank=True)
    response = models.TextField("回答", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.subject
