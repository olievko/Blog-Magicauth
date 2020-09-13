from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from posts.models import Post, Comment
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.db.models import Count
from taggit.models import Tag
from posts.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request, tag_slug=None):
    template = 'blog/post/list.html'
    count = User.objects.count()
    posts = Post.published.all()
    common_tags = Post.tags.most_common()[:4]
    tags = Post.tags.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    # PAGINATION
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'count': count,
        'page': page,
        'posts': posts,
        'tag': tag,
        'tags': tags,
        'common_tags': common_tags,
    }
    return render(request, template, context)


@login_required
def post_detail(request, year, month, day, post):
    template = 'blog/post/detail.html'
    count = User.objects.count()
    posts = Post.published.all()
    tags = Post.tags.all()
    common_tags = Post.tags.most_common()[:4]

    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    images = post.images.all()

    initial_data = {
        "content_type": post.get_content_type,
        "object_id": post.id
    }
    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
        content_type = post.get_content_type
        obj_id = post.id
        content_data = comment_form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = post.comments

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]

    context = {
        'count': count,
        'tags': tags,
        'common_tags': common_tags,
        'post': post,
        'posts': posts,
        'images': images,

        'comments': comments,
        'comment_form': comment_form,

        'similar_posts': similar_posts
    }
    return render(request, template, context)


class PostsSearch(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Post.published.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        context["count"] = User.objects.count()
        context["tags"] = Post.tags.all()
        context["common_tags"] = Post.tags.most_common()[:4]
        return context