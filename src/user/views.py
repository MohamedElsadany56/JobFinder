from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout as auth_logout
from django.core.mail import send_mail
from .models import Profile
from task.models import Task, Apply
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
def signup(request):
    if request.method == "POST":
        username = request.POST.get("UserName")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validation
        errors = []
        if password != confirm_password:
            errors.append("Passwords do not match.")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")
        if User.objects.filter(username=username).exists():
            errors.append("Username is already taken.")
        if User.objects.filter(email=email).exists():
            errors.append("Email is already registered.")

        if errors:
            return render(request, "registration/signup.html", {"errors": errors})

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password)
        profile, _ = Profile.objects.get_or_create(user=user)  # Ensure Profile is created
        profile.generate_otp()

        # Send OTP
        send_mail(
            subject="Verify your email",
            message=f"Your OTP code is {profile.otp}.",
            from_email="your-email@example.com",
            recipient_list=[email],
            fail_silently=False,
        )

        # Store email in session
        request.session['email'] = email

        # Redirect to OTP verification page
        return redirect("user:verify_email")

    return render(request, "registration/signup.html")


def verify_email(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        email = request.session.get("email")  # Safely get the email from the session

        if not email:
            return render(request, "user/verify_email.html", {"error": "Session expired. Please sign up again."})

        try:
            user = User.objects.get(email=email)
            profile = user.profile
            if profile.otp == otp:
                profile.is_verified = True
                profile.otp = None  # Clear the OTP after verification
                profile.save()

                # Log the user in after successful verification
                login(request, user)

                # Safely delete session key
                request.session.pop("email", None)

                return redirect("user:profile", username=user.username)  # Redirect to profile
            else:
                return render(request, "user/verify_email.html", {"error": "Invalid OTP"})
        except User.DoesNotExist:
            return render(request, "user/verify_email.html", {"error": "User not found"})

    return render(request, "user/verify_email.html")


def profile(request, username):

    # Retrieve the user and dynamically create their profile if it doesn't exist
    user = get_object_or_404(User, username=username)
    user_profile, _ = Profile.objects.get_or_create(user=user)

    # Get tasks created by the user
    created_tasks = Task.objects.filter(owner=user)

    # Get tasks the user has applied for
    applied_tasks = Apply.objects.filter(applicant=user)
    # Render the profile page with the retrieved data
    return render(request, 'user/ProfilePage.html', {
        'profile': user_profile,
        'created_tasks': created_tasks,
        'applied_tasks': applied_tasks,
    })


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create a Profile for a new User.
    """
    if created:
        Profile.objects.get_or_create(user=instance)



