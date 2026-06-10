from django.urls import path
from django.contrib.auth import views as auth_views  # Tayyor viewlarni import qilamiz
from . import views 
from .views import (
    TaskListCreateAPIView, 
    TaskRetrieveUpdateDestroyAPIView,
    RegisterAPIView,
    LoginAPIView,
    TaskStatusUpdateAPIView
)
urlpatterns = [
    path('', views.HomeView, name='todo_home'),
    path('tasks', views.TaskListView, name = "task_list"),
    path('tasks/create/', views.TaskCreateView, name='task_create'),
    path('tasks/update/<int:task_id>/', views.TaskUpdateView, name='task_update'),
    path('profile/', views.ProfileView, name='profile'),
    path('tasks/change-status/<int:task_id>/<str:new_status>/', views.change_status, name='change_status'),
    path('login/', auth_views.LoginView.as_view(template_name='task/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView, name = "register"),
    # API
    path('api/auth/register/', RegisterAPIView.as_view(), name = 'api_register'),
    path('api/auth/login/', LoginAPIView.as_view(), name = "api_login"),
    path('api/tasks/', TaskListCreateAPIView.as_view(), name = "api_task_list"),
    path('api/tasks/<int:id>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name = "api_taks_detail"),
    
    path('api/tasks/<int:id>/status/', TaskStatusUpdateAPIView.as_view(), name = "api_task_status_update"),
]