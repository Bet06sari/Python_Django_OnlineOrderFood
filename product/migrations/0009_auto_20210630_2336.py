# Generated by Django 3.1.7 on 2021-06-30 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20210620_0111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='level',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='tree_id',
        ),
    ]
