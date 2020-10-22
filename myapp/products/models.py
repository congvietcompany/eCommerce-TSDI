import random
import os
from io import BytesIO
from django.core.files import File
from django.db import models
from PIL import Image
from django.contrib.auth.models import User

from . utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)

    return name, ext


def upload_image_path_category(instance, filename):
    new_filename = random.randint(1, 23243423)
    name, ext = get_filename_ext(filename)
    final_filename ='{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)

    #return "products/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

    return "category/{final_filename}".format(final_filename=final_filename)
    # end create path and images


def upload_image_path_product(instance, filename):
    new_filename = random.randint(1, 23243423)
    name, ext = get_filename_ext(filename)
    final_filename ='{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)

    #return "products/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

    return "products/{final_filename}".format(final_filename=final_filename)
    # end create path and images


class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_image_path_category, null=True, blank=True)
    ordering = models.IntegerField(default=1)
    available = models.BooleanField(default=False)
    feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_slural = 'Categories'

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return '/%s/' % (self.slug)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='variants', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    request = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0.0)
    sale_price = models.FloatField(default=0.0)
    image = models.ImageField(upload_to=upload_image_path_product, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=upload_image_path_product, null=True, blank=True)

    feature = models.BooleanField(default=False)
    available = models.BooleanField(default=False)
    num_available = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        print('Save', self.image.path)
        self.thumbnail = self.make_thumbnail(self.image)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    def get_rating(self):
        total = sum(int(review['stars']) for review in self.reviews.values())
        if self.reviews.count() > 0:
            return total / self.reviews.count()
        else:
            return 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_path_product, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=upload_image_path_product, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.thumbnail = self.make_thumbnail(self.image)

        super().save(*args, **kwargs)

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)

    content = models.TextField(blank=True, null=True)
    stars = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

