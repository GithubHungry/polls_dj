from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, PostShots, Review


# Register your models here.
class ReviewInline(admin.TabularInline):
	"""For add reviews to posts."""
	model = Review
	extra = 1  # Number of extra reviews.
	readonly_fields = ('name', 'email',)


class PostShotsInLine(admin.TabularInline):
	model = PostShots
	extra = 3

	def get_image(self, obj):
		return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

	get_image.short_description = 'Image'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'author', 'get_poster', 'publish', 'status')
	list_display_links = ('id', 'title')
	list_filter = ('status', 'created', 'publish', 'author')
	search_fields = ('title', 'body')
	prepopulated_fields = {'slug': ('title',)}  # auto generate slug from title
	raw_id_fields = ('author',)
	date_hierarchy = 'publish'
	ordering = ('status', 'publish')
	inlines = [PostShotsInLine, ReviewInline]

	def get_poster(self, obj):
		"""Show mini photo of book."""
		return mark_safe(f'<img src={obj.poster.url} width="90" height="110"')

	get_poster.short_description = 'Poster'


@admin.register(PostShots)
class PostShotsAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'get_image',)
	list_display_links = ('title',)
	search_fields = ('title',)
	readonly_fields = ('get_image',)

	def get_image(self, obj):
		"""Show mini photo of book."""
		return mark_safe(f'<img src={obj.image.url} width="50" height="70"')

	get_image.short_description = 'Image'


@admin.register(Review)
class Review(admin.ModelAdmin):
	list_display = ('id', 'name', 'email', 'post', 'created', 'active')
	list_display_links = ('id', 'name', 'email')
	search_fields = ('name', 'post', 'body', 'email')
