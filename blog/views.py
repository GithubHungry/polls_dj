from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.postgres.search import SearchVector
from taggit.models import Tag

from .forms import EmailPostForm, ReviewForm, SearchForm
from .models import Post, Review


# Create your views here.

# class PostListView(ListView):
# 	queryset = Post.published.all()
# 	context_object_name = 'posts'  # how it names in template
# 	template_name = 'blog/post/list.html'
# 	paginate_by = 3


def post_list(request, tag_slug=None):
	object_list = Post.published.all()
	tag = None
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])
	paginator = Paginator(object_list, 3)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


# class PostDetailView(DetailView):
# 	model = Post
# 	template_name = 'blog/post/detail.html'
#
# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		return context


def post_share(request, slug):
	post = get_object_or_404(Post, status='published', slug=slug)
	sent = False
	if request.method == 'POST':
		form = EmailPostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			title_text = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
			text = 'Read "{}" at {} \n\n {}\' comments: {}'.format(post.title, post_url, cd['name'], cd['comment'])
			send_mail(title_text, text, 'shopmanage7@gmail.com', [cd['to']], False)
			sent = True
	else:
		form = EmailPostForm()
	return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_detail(request, slug, year, month, day):
	"""Add new review."""
	post = get_object_or_404(Post, slug=slug, status='published', publish__year=year, publish__month=month,
	                         publish__day=day)
	reviews = post.reviews.filter(active=True)
	new_review = None
	if request.method == 'POST':
		review_form = ReviewForm(data=request.POST)
		if review_form.is_valid():
			new_review = review_form.save(commit=False)
			if request.POST.get('parent', None):
				review_form.parent_id = int(request.POST.get('parent'))
			new_review.post = post
			new_review.save()
	else:
		review_form = ReviewForm()

	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.published.filter(tags__in=post_tags_ids)
	similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

	return render(request, 'blog/post/detail.html',
	              {'post': post, 'reviews': reviews, 'review_form': review_form, 'new_review': new_review,
	               'similar_posts': similar_posts})


def post_search(request):
	form = SearchForm()
	query = None
	results = []
	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['query']
			results = Post.objects.annotate(search=SearchVector('title', 'body')).filter(search=query)
	return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})
