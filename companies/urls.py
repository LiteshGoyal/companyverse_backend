from django.urls import path
from .views import CreateCompanyView, AddEmployeeView, CompanyEmployeesView, EmployeeDetailView, UpdateEmployeeRoleView, RemoveEmployeeView

urlpatterns=[
    path('create/',CreateCompanyView.as_view(), name="create_company_view"),
    path('add-employee/',AddEmployeeView.as_view(), name="add_employee_view"),
    path(
        "employees/",
        CompanyEmployeesView.as_view(),
        name="company_employees_view"
    ),
    path(
        "employees/<str:pk>/",
        EmployeeDetailView.as_view(),
        name="employee_detail_view"
    ),
    path(
        "employees/<uuid:pk>/update-role/",
        UpdateEmployeeRoleView.as_view(),
        name="update_employee_role_view"
    ),
    path(
        "employees/<uuid:pk>/remove/",
        RemoveEmployeeView.as_view(),
        name="remove_employee_view"
    ),
]