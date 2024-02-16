from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from .forms import AddPost
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from blogmain.models import Post
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    posts = Post.objects.all()
    return render(request, 'blogmain/home.html', {'posts': posts})

def about(request):
    return render(request, 'blogmain/about.html')

class HomeViewSet(ListView):
    template_name = 'blogmain/home.html'
    context_object_name = 'posts' 
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.select_related('author'). \
        select_related('author__profile').all().order_by('-date_posted')
        return queryset


class UserPostListView(ListView):
    template_name = 'blogmain/user_posts.html'
    context_object_name = 'posts'  
    paginate_by = 5

    def get_queryset(self):
        user_username = self.kwargs['username']
        user = User.objects.get(username=user_username)
        queryset = Post.objects.select_related('author'). \
        select_related('author__profile').filter(author=user).order_by('-date_posted')
        return list(queryset)
    
  
    
class AboutViewSet(TemplateView):
    template_name = 'blogmain/about.html'


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'    


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = AddPost
    # get_absolute_url method inside the Post model class handles the redirecting
    # success_url = '/'
    template_name = 'blogmain/post_form.html'



    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = AddPost
    # get_absolute_url method inside the Post model class handles the redirecting
    # success_url = '/'
    template_name = 'blogmain/post_form.html'



    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blogmain/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
