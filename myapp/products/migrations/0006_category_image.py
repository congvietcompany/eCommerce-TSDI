# Generated by Django 3.1.1 on 2020-09-20 02:17

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20200920_0750'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=products.models.upload_image_path_category),
        ),
    ]
