from django.db import models
from taskCreator.models import TaskCreator
from django.contrib.auth.models import User

task_status=(
    ('new','New'),
    ('inprogress','Inprogress'),
    ('finished','Finished'),
    ('canceled','Canceled')
)
class Task (models.Model):

    title = models.CharField(max_length=30)
    taskDescription =models.TextField(max_length = 1500 )
    publishedAt = models.DateTimeField(auto_now = True)
    taskDeadline = models.DateTimeField(auto_now = True)
    taskStatus = models.TextField(max_length=30,choices=task_status)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    # location to be added
    # list of applicants
    def __str__(self):
        return self.title

# class ListApplicants(models.Model):
#     name =  models.CharField(max_length=30)
#     def __str__(self):
#         return self.name

def updateStatus ():
    pass
    
def addApplicant ():
    pass