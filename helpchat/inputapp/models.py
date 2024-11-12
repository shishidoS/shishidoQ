from django.db import models

class Inquiry(models.Model):
    company = models.CharField(max_length=100, verbose_name="会社名")
    store = models.CharField(max_length=100, verbose_name="店舗名")
    staff = models.CharField(max_length=100, verbose_name="担当スタッフ")
    subject = models.CharField(max_length=100, verbose_name="題名")
    message = models.TextField(verbose_name="問い合わせ内容")
    response = models.TextField(verbose_name="回答内容", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

    def __str__(self):
        return f"{self.subject} - {self.company} ({self.created_at})"
