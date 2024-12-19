from django.shortcuts import render

def homepage(request):
    return render(request, 'index.html')
def howitworks(request):
    return render(request, 'howitworks.html')