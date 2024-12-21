from django.http import Http404
from django.shortcuts import render, redirect
from .models import Task
from .form import postTask ,ApplyForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')
@login_required
def post_task(request):
    if request.method == 'POST':
        form = postTask(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user  # Assign the task owner to the logged-in user
            task.save()
            print("done")
            return redirect('tasks:taskList')  # Update with an appropriate redirect
        else:
            print(form.errors)  # This will print out any form validation errors
    else:
        form = postTask()  # Show an empty form for GET requests
    return render(request, 'task/postTask.html', {'form': form})

# def task_list (request):
#     task_list = Task.objects.all()
#     context = {'tasks':task_list}
#     return render(request,'task/taskList.html',context)
def task_list(request):
    tasks = Task.objects.all()

    # Apply filters
    keyword = request.GET.get('keyword', '')
    if keyword:
        tasks = tasks.filter(title__icontains=keyword)

    location = request.GET.get('location', '')
    if location:
        tasks = tasks.filter(location=location)

    category = request.GET.get('category', '')
    if category:
        tasks = tasks.filter(category=category)

    # Sorting logic
    sort_by = request.GET.get('sort', 'recent')
    if sort_by == 'recent':
        tasks = tasks.order_by('-publishedAt')  # Assuming publishedAt is the field to sort by
    elif sort_by == 'oldest':
        tasks = tasks.order_by('publishedAt')

    context = {'tasks': tasks}
    return render(request, 'task/TaskList.html', context)



def task_detail(request, slug):
    if not slug:  # Check if slug is None or empty
        raise Http404("Invalid task slug.")
    
    try:
        task_detail = Task.objects.get(slug=slug)
    except Task.DoesNotExist:
        raise Http404("Task matching query does not exist.")
    


    if request.method == 'POST':
        form = ApplyForm(request.POST)
        print("in form")
        if form.is_valid():
            myform = form.save(commit=False)
            myform.Task = task_detail
            myform.applicant = request.user
            myform.save()
            print("Application submitted successfully")
        else:
            print("Form is not valid")

    else :
        form = ApplyForm()


    context = {'task': task_detail , 'form': form}
    return render(request, 'task/ApplyTask.html', context)




