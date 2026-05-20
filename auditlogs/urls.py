from django.urls import path

from .views import (
    CompanyAuditLogsView
)

urlpatterns = [

    path(
        "company/",
        CompanyAuditLogsView.as_view(),
        name="company_audit_logs_view"
    ),
]