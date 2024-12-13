from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class TaskCreator (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='task_creator')
    

    def __str__(self):
            return self.User.name



def postTask ():
    pass
    
def manageTask ():
    pass
    
