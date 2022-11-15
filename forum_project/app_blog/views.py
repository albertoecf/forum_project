from django.shortcuts import render
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
