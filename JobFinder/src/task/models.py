from django.db import models
from taskCreator.models import TaskCreator
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid
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
    deadline = models.DateTimeField(null=True)  # Deadline field
    publishedAt = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it's empty
            self.slug = slugify(self.title)
        super(Task, self).save(*args, **kwargs)

 
    # location to be added
    # list of applicants


# class ListApplicants(models.Model):
#     name =  models.CharField(max_length=30)
#     def __str__(self):
#         return self.name


class Apply(models.Model):
    Task = models.ForeignKey(Task, related_name='apply_job', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)



    def __str__(self):
        return self.name



    def __str__(self):
        return self.name

def updateStatus ():
    pass
    
def addApplicant ():
    pass