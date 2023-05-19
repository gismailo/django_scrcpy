# Generated by Django 3.2.18 on 2023-05-19 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0005_auto_20230519_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='details',
            field=models.TextField(blank=True, verbose_name='备注信息'),
        ),
        migrations.AddField(
            model_name='picture',
            name='name',
            field=models.CharField(blank=True, max_length=32, verbose_name='名称'),
        ),
        migrations.AddField(
            model_name='picture',
            name='updated_time',
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间'),
        ),
        migrations.AddField(
            model_name='video',
            name='details',
            field=models.TextField(blank=True, verbose_name='备注信息'),
        ),
        migrations.AddField(
            model_name='video',
            name='name',
            field=models.CharField(blank=True, max_length=32, verbose_name='名称'),
        ),
        migrations.AddField(
            model_name='video',
            name='updated_time',
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间'),
        ),
    ]
