from django.shortcuts import render, redirect
from .models import Task
from .form import postTask

def index(request):
    return render(request, 'index.html')

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

def task_list (request):
    task_list = Task.objects.all()
    context = {'tasks':task_list}
    return render(request,'task/taskList.html',context)



def task_detail(request,id):
    task_detail = Task.objects.get(id=id)
    context = {'tasks':task_detail}
    return render(request,'task/taskDetail.html',context)