from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class PublishedManager(models.Manager):
	"""Create model manager."""

	def get_queryset(self):  # Look like objects, but with filter published
		return super().get_queryset().filter(status='published')


class Post(models.Model):
	"""Post model"""
	STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
	title = models.CharField(max_length=225)
	poster = models.ImageField(upload_to='posts/', blank=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	slug = models.SlugField(max_length=225, unique_for_date='publish')
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	objects = models.Manager()  # Default manager
	published = PublishedManager()  # Custom manager

	class Meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'
		ordering = ('-publish',)

	def __str__(self):
		return self.title


class PostShots(models.Model):
	"""Post shot model."""
	title = models.CharField(max_length=225)
	description = models.TextField()
	image = models.ImageField(upload_to='book_shots/')
	post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'Post images'
		verbose_name = 'Post image'

	def __str__(self):
		return self.title
