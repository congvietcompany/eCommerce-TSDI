# Generated by Django 3.1.1 on 2020-10-01 09:58

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_remove_productimage_thumbnail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='content',
            new_name='request',
        ),
        migrations.AddField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=products.models.upload_image_path_product),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
