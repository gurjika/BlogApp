from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.views.generic import CreateView, FormView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . forms import (
    RegisterForm, 
    UserUpdateForm, 
    ProfileUpdateForm
)

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f"User {username} created")
            form.save()
            return redirect('blog-home')
        
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})
    # in the class based view below this is exaclty what we did

class RegisterViewSet(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    model = User

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        messages.success(request=self.request, message=f"User {username} created")
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return '/login'
    

class MyLoginView(LoginView):
    template_name = 'users/login.html'

    next_page = 'blog-home'

class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'users/logout.html')

@login_required
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=current_user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=current_user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=current_user)
        profile_form = ProfileUpdateForm(instance=current_user.profile)

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'users/profile.html', context)


class MyPasswordResetView(auth_views.PasswordResetView):
    template_name = 'users/password_reset.html'
