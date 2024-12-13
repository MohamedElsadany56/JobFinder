from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('index/', views.index, name='Home'),
    path('post/', views.post_task, name='postTask'),
    path('', views.task_list, name='taskList'),
    path('<int:id>',views.task_detail),
]
