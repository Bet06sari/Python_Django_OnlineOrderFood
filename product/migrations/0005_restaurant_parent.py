# Generated by Django 3.1.7 on 2021-06-19 20:25

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_remove_restaurant_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.restaurant'),
        ),
    ]
