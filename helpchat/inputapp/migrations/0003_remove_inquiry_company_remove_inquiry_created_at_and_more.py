# Generated by Django 5.1 on 2025-05-09 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inputapp', '0002_remove_inquiry_answer_inquiry_response_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inquiry',
            name='company',
        ),
        migrations.RemoveField(
            model_name='inquiry',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='inquiry',
            name='staff',
        ),
        migrations.RemoveField(
            model_name='inquiry',
            name='store',
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='message',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='response',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='subject',
            field=models.CharField(max_length=200),
        ),
    ]
