from django.urls import path
from .views import CreateTaskView, MyTasksView, UpdateTaskStatusView, ViewCompanyTasks

urlpatterns = [
    path('create/', CreateTaskView.as_view(),name="create_task_view"),
    path('my-tasks/',MyTasksView.as_view(), name = "my_tasks_view"),
    path('<int:pk>/update-status/', UpdateTaskStatusView.as_view(), name="update_task_status_view"),
    path('company-tasks/', ViewCompanyTasks.as_view(), name="view_company_tasks")
]