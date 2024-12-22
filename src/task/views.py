from django.http import Http404
from django.shortcuts import render, redirect
from .models import Task ,Apply
from .form import postTask ,ApplyForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden



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
            return redirect('tasks:taskList')  # Redirect to the task list page
        else:
            print(form.errors)  # Print out any form validation errors
    else:
        form = postTask()  # Show an empty form for GET requests
    return render(request, 'task/postTask.html', {'form': form})



def view_applicants(request, slug):
    task = get_object_or_404(Task, slug=slug)
    applicants = Apply.objects.filter(Task=task)
    
    context = {
        'task': task,
        'applicants': applicants,
    }
    return render(request, 'task/Application_list.html', context)


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

    disability = request.GET.get('disability', '')
    if disability:
        tasks = tasks.filter(disability=disability)

    # Sorting logic
    sort_by = request.GET.get('sort', 'recent')
    if sort_by == 'recent':
        tasks = tasks.order_by('-publishedAt')  # Assuming `publishedAt` is the field for sorting
    elif sort_by == 'oldest':
        tasks = tasks.order_by('publishedAt')

    # Pass filters back to template for persistence
    context = {
        'tasks': tasks,
        'locations': Task.objects.values_list('location', flat=True).distinct(),
        'categories': Task.objects.values_list('category', flat=True).distinct(),
        'request': request,
    }
    return render(request, 'task/TaskList.html', context)




def task_detail(request, slug):
    try:
        task_detail = Task.objects.prefetch_related('apply_job').get(slug=slug)
        applicants = Apply.objects.filter(Task=task_detail)  # Retrieve applicants for this task
    except Task.DoesNotExist:
        raise Http404("Task matching query does not exist.")
    
    if request.method == 'POST':
        form = ApplyForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.Task = task_detail
            myform.applicant = request.user
            myform.save()
        else:
            print("Form is not valid")
    else:
        form = ApplyForm()

    context = {
        'task': task_detail,
        'form': form,
        'Applys': applicants  # Pass applicants queryset
    }
    return render(request, 'task/ApplyTask.html', context)

from django.shortcuts import redirect

def update_applicant_status(request, applicant_id, action):
    applicant = get_object_or_404(Apply, id=applicant_id)
    task = applicant.Task  # Get the associated task

    # Verify if the logged-in user is the task owner
    if request.user != task.owner:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    task_title = task.title  # Get the task title
    employer_email = task.owner.email  # Get the employer's email

    if action == "approve":
        applicant.status = "Approved"
        message = (
            f"Your application for the task '{task_title}' has been approved. Congratulations!\n\n"
            f"You can contact the employer at: {employer_email}."
        )
    elif action == "reject":
        applicant.status = "Rejected"
        message = (
            f"We regret to inform you that your application for the task '{task_title}' has been rejected.\n\n"
            f"If you have any questions, you can contact the employer at: {employer_email}."
        )
    else:
        raise Http404("Invalid action.")

    # Save the status update
    applicant.save()

    # Send an email to the applicant
    if applicant.applicant and applicant.applicant.email:
        send_mail(
            subject=f"Application Status Update for Task: {task_title}",
            message=message,
            from_email="jobfinder991@gmail.com",
            recipient_list=[applicant.applicant.email],
            fail_silently=False,
        )

    # Redirect back to the applicants list
    return redirect('tasks:view_applicants', slug=task.slug)
