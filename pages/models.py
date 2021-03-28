from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

import sys

from PIL import Image
from io import BytesIO 
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

User = get_user_model()

def get_product_url(obj, viewname):
	ct_model = obj.__class__._meta.model_name
	return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})

class Category(models.Model):
	name = models.TextField(max_length = 200, verbose_name = 'Категория')
	image = models.ImageField(null=True, verbose_name='Картинка')
	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.slug

	def get_absolute_url(self):
		return reverse('category_detail', kwargs={'slug': self.slug})

class Post(models.Model):

	title = models.CharField(max_length = 1000, verbose_name = 'Наименование')
	category = models.ForeignKey(
		Category,
		on_delete = models.CASCADE,#POTECT\CASCADE\DO_NOTHING
		verbose_name = 'Категория',
		null=True
	)
	image = models.ImageField(null=True, verbose_name = 'Привествующая картинка\n(высота = 320px)')
	date = models.DateTimeField(null=True, verbose_name = 'Дата публикации')
	body = RichTextField(null=True, verbose_name='Содержание статьи')
	view = models.IntegerField(null=True, default=0, verbose_name='Кол-во просмотров')
	autor = models.TextField(null=True, verbose_name = 'Автор публикации')
	ip = models.GenericIPAddressField(verbose_name='IP пользователей')

	def __str__(self):
		return self.title

class TopPost(models.Model):
	Post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name='Одна из лучших статей')

	def __str__(self):
		return self.Post.title