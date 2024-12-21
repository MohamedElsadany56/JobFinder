from django.db import models
from taskCreator.models import TaskCreator
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid
from django.utils import timezone
class Task (models.Model):

    CATEGORY_CHOICES = [
        ('home_repair', 'Home Repair'),
        ('delivery', 'Delivery'),
        ('tutoring', 'Tutoring'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=30)
    taskDescription = models.TextField(max_length=1500,null=False)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=False,default='other')
    location = models.CharField(max_length=100, blank=True,default='')  # Optional field
    budget = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)  # Budget in $
    deadline = models.DateTimeField(null=True) 
    publishedAt = models.DateTimeField(auto_now_add=True )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    applicants = models.ManyToManyField(User, related_name='applied_tasks', through='Apply') # Many to many relationship with User 
    
    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)  
        if not self.slug:
            self.slug = f"{slugify(self.title)}-{self.id}"
            super(Task, self).save(*args, **kwargs) 


class Apply(models.Model):
    Task = models.ForeignKey(Task, related_name='apply_job', on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apply_job', null=True, blank=True)
    name = models.CharField(max_length=50)
    experience= models.TextField(max_length=100)
    desired_price=models.IntegerField()
    # has_disability = models.BooleanField(default=False)  # New field
    # disability_description = models.TextField(blank=True, null=True)  # Optional for disability details

    
    def __str__(self):

        return f"{self.applicant.username} applied for {self.Task.title}"


# class Application(models.Model):
#     task = models.ForeignKey(Task, related_name='applications', on_delete=models.CASCADE)
#     applicant = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)
#     applied_at = models.DateTimeField(auto_now_add=True)  

#     def __str__(self):
#         return f"{self.applicant.username} applied for {self.task.title}"


def updateStatus ():
    pass
    
def addApplicant ():
    pass