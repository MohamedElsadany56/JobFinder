from django import forms

from .models import Task




class postTask(forms.ModelForm):
    class Meta:
       model = Task
       fields = ['title', 'taskDescription', 'category', 'location', 'budget', 'deadline']
