from django import forms

from .models import Task , Apply




class postTask(forms.ModelForm):
    class Meta:
       model = Task
       fields = ['title', 'taskDescription', 'category', 'location', 'budget', 'deadline']
class ApplyForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = ['name']