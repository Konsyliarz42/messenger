from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import User, Profile, Conversation
from .forms import RegisterForm, LoginForm, EditProfileForm

TEMPLATES = {
    'index': "home.html",
    'profile': 'profile.html',
    'conversation': 'conversation.html'
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

    context = {
        'users': User.objects.all(),
        'profiles': Profile.objects.all(),
        'r_form': r_form,
        'l_form': l_form
    }

    return render(request, TEMPLATES['index'], context)

@login_required
def profile(request):
    form = EditProfileForm(request.user, initial={
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'description': request.user.profile.description
    })

    if request.method == 'POST':
        form_variant = request.POST.get('form')
        
        # Edit user
        if form_variant == 'edit':
            form = EditProfileForm(request.user, request.POST)
            first_name = request.POST.get('first_name') or None
            last_name = request.POST.get('last_name') or None
            email = request.POST.get('email') or None
            password = request.POST.get('new_password') or None
            description = request.POST.get('description') or None

            if form.is_valid():
                user = request.user

                if first_name:
                    user.first_name = first_name
                    user.save()
                
                if last_name:
                    user.last_name = last_name
                    user.save()

                if email:
                    user.email = email
                    user.save()

                if password:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)

                if description:
                    user.profile.description = description
                    user.profile.save()

                user = authenticate(request,
                    username=request.POST.get('username'),
                    password=request.POST.get('new_password')
                )

                if user:
                    login(request, user)

        # Add friend
        if form_variant == 'add_friend':
            profile = request.user.profile
            user = User.objects.get(id=request.POST.get('user_id'))
            profile.friends.add(user)
            profile.save()

        # Remove friend
        if form_variant == 'remove_friend':
            profile = request.user.profile
            user = User.objects.get(id=request.POST.get('user_id'))
            profile.friends.remove(user)
            profile.save()


        # Start conversation
        if form_variant == 'conversation':
            user_id = int(request.POST.get('user_id'))
            user = User.objects.get(id=user_id)
            user_conversations = [c for c in user.profile.conversations.all() if len(c.members.all()) == 2]
            old_conversation = [c for c in user_conversations if request.user in c.members.all()]

            if old_conversation:
                return redirect(f'/conversation/{old_conversation[0].id}')

            conversation = Conversation(start_conversation=datetime.now())
            conversation.save()
            
            conversation.members.add(request.user)
            conversation.members.add(user)
            conversation.save()

            request.user.profile.conversations.add(conversation)
            request.user.profile.save()

            user.profile.conversations.add(conversation)
            user.profile.save()

            return redirect(f'/conversation/{conversation.id}')

    context = {
        'users': User.objects.all(),
        'friends': request.user.profile.friends.all(),
        'conversations': request.user.profile.get_conversations(),
        'form': form
    }

    return render(request, TEMPLATES['profile'], context)


@login_required
def conversation(request, conversation_id):

    conversation = Conversation.objects.get(id=conversation_id)

    if request.user not in conversation.members.all():
        return redirect(f'/home')
    
    if request.method == 'POST':
        conversation.add_entry(request.user, request.POST.get('message'))
        conversation.save()

    context = {
        'members': conversation.members,
        'entries': conversation.get_entries()
    }

    return render(request, TEMPLATES['conversation'], context)