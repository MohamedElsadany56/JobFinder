from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.mail import send_mail
from .models import Profile
from task.models import Task
from django.contrib.auth import login
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
        profile = user.profile
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
                if "email" in request.session:
                    del request.session["email"]

                return redirect("user:profile")  # Redirect to profile
            else:
                # Ensure that the error message is passed into the context correctly
                return render(request, "user/verify_email.html", {"error": "Invalid OTP"})
        except User.DoesNotExist:
            return render(request, "user/verify_email.html", {"error": "User not found"})

    return render(request, "user/verify_email.html")




def profile(request):
    profile = Profile.objects.get(user=request.user)
    tasks = Task.objects.filter(owner=request.user)
    return render(request, 'user/ProfilePage.html', {'profile': profile, 'tasks': tasks})
