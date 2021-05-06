from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout

from .models import User, Profile
from .forms import RegisterForm, LoginForm

TEMPLATES = {
    'index': "index.html"
}

def index(request):
    r_form = RegisterForm()
    l_form = LoginForm()

    if request.method == 'POST':
        form_variant = request.POST.get('form')
        
        # Register new user
        if form_variant == 'register':
            r_form = RegisterForm(request.POST)

            if r_form.is_valid():
                r_form = RegisterForm()

                User.objects.create_user(
                    username=request.POST.get('username'),
                    email=request.POST.get("email"),
                    password=request.POST.get('password')
                ).save

        # Login user
        if form_variant == 'login':
            l_form = LoginForm(request.POST)

            if l_form.is_valid():
                l_form = LoginForm()

                user = authenticate(request,
                    username=request.POST.get('username'),
                    password=request.POST.get('password')
                )

                if user:
                    login(request, user)

                    # logout after end session
                    if not request.POST.get('remember_me'):
                        request.session.set_expiry(0)

        # Logout user
        if form_variant == 'logout':
            logout(request)

        # Add friend
        if form_variant == 'add_friend':
            profile = request.user.profile
            profile.add_friend(request.POST.get('user_id'))
            profile.save()

        # Remove friend
        if form_variant == 'remove_friend':
            profile = request.user.profile
            profile.remove_friend(request.POST.get('user_id'))
            profile.save()

    context = {
        'users': User.objects.all(),
        'profiles': Profile.objects.all(),
        'r_form': r_form,
        'l_form': l_form
    }

    return render(request, TEMPLATES['index'], context)