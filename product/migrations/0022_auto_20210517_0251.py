# Generated by Django 3.1.7 on 2021-05-16 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_auto_20210517_0246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='comment',
            name='subject',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='comment',
            name='update_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]