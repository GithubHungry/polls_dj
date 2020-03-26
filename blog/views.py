from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView

from .forms import EmailPostForm
from .models import Post


# Create your views here.

class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'  # how it names in template
	template_name = 'blog/post/list.html'
	paginate_by = 3


# def post_list(request):
# 	object_list = Post.published.all()
# 	paginator = Paginator(object_list, 3)
# 	page = request.GET.get('page')
# 	try:
# 		posts = paginator.page(page)
# 	except PageNotAnInteger:
# 		posts = paginator.page(1)
# 	except EmptyPage:
# 		posts = paginator.page(paginator.num_pages)
# 	return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/post/detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context


# def post_detail(request, slug, year, month, day):
# 	post = get_object_or_404(Post, slug=slug, status='published', publish__year=year, publish__month=month,
# 	                         publish__day=day)
# 	return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
	post = get_object_or_404(Post, status='published', id=post_id)
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
