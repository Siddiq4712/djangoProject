from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required # Import this
from .forms import UserRegisterForm, UserLoginForm
from .models import Profile # Import Profile
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.utils.safestring import mark_safe
from notifications.utils import send_welcome_email

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_welcome_email(user)
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('user_login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Register'})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('book_list') # Redirect to the book list page
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form, 'title': 'Login'})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('user_login')

@login_required
def profile(request):
    """
    Displays the current user's profile information.
    """
    return render(request, 'users/profile.html', {'title': 'Profile'})

@login_required
def library_card(request):
    """
    Generates and displays a digital library card with user info and QR code.
    """
    user_profile = get_object_or_404(Profile, user=request.user)
    
    # Data to encode in QR code (e.g., user's membership ID)
    qr_data = f"MEMBERSHIP_ID:{user_profile.membership_id}" 

    # Generate QR code as SVG
    factory = qrcode.image.svg.SvgPathImage # For a cleaner SVG
    img = qrcode.make(qr_data, image_factory=factory, box_size=5)
    
    # Save SVG to a buffer
    stream = BytesIO()
    img.save(stream)
    
    # Get SVG string and mark it safe for rendering in template
    svg_qr_code = mark_safe(stream.getvalue().decode('utf-8'))

    context = {
        'title': 'Digital Library Card',
        'user_profile': user_profile,
        'svg_qr_code': svg_qr_code,
    }
    return render(request, 'users/library_card.html', context)
