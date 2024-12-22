from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

def homepage(request):
    return render(request, 'index.html')
def howitworks(request):
    return render(request, 'howitworks.html')
def logout(request):
    auth_logout(request)
    return redirect("/")
