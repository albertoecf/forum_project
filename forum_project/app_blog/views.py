from django.shortcuts import (render, gert_object_or_404,
                            redirect)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from app_blog.forms import PostFormModel, CommentFormModel
from django.views.generic import (TemplateView,
                                    Listview, DetailView,
                                    CreateView, UpdateView,
                                    DeleteView)
from app_blog import PostModel, CommentModel
# Create your views here.

class AboutView(TemplateView):
    template_name = "about_file.html"

class PostListView(ListView):
    model = PostModel

    def get_queryset(self):
        return PostModel.objects.filter(
                                        published_date__lte=timezone.now(
                                        )).order_by('-published_date')

class PostDetailView(DetailView):
    model = PostModel

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'app_blog/post_detail.html'
    form_class = PostFormModel
    model = PostModel

class PostUpdateView(LoginRequiredMixin, Update):
    login_url = '/login/'
    redirect_field_name = 'app_blog/post_detail.html'
    form_class = PostFormModel
    model = PostModel

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = PostModel
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url =  '/login/'
    redirect_field_name = 'app_blog/post_list.html'

    def get_queryset(self):
        return PostModel.objects.filter(
                                        published_date__isnull=True).order_by('-published_date')

@login_required
def post_publish(request,pk):
    post = gert_object_or_404(Post, pk=pk)
    post.publish
    return redirect('post_detail',pk=pk)

@login_required
def add_comment_to_post(request,pk):
    post = gert_object_or_404(PostModel, pk=pk)
    if request.method == 'POST':
        form = CommentFormModel(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentFormModel()
    return render(request, 'app_blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request,pk):
    comment = gert_object_or_404(CommentModel, pk=pk)
    comment.approve()
    return redirect('post_detail', pk = comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = gert_object_or_404(request, pk):
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)
