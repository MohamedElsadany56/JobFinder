from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('post/', views.post_task, name='postTask'),
    path('', views.task_list, name='taskList'),
    path('tasks/<str:slug>/', views.task_detail, name='taskDetail'),
    path('<int:id>',views.task_detail,name='taskDetail'),
]
