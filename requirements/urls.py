from django.urls import path
from .views import CreateRequirementView, MarketplaceRequirementsView, RespondToRequirementView, ViewRequirementResponsesView, UpdateRequirementResponseStatusView, CloseRequirementView, MyRequirementsView

urlpatterns = [
    path(
        "create/",
        CreateRequirementView.as_view(),
        name="create_requirement_view"
    ),
    path(
        "my-requirements/",
        MyRequirementsView.as_view(),
        name="my_requirements"
    ),
    path(
    "marketplace/",
    MarketplaceRequirementsView.as_view(),
    name="marketplace_requirements_view"
    ),
    path(
        "<int:pk>/respond/",
        RespondToRequirementView.as_view(),
        name="respond_to_requirement_view"
    ),
    path(
        "<int:pk>/responses/",
        ViewRequirementResponsesView.as_view(),
        name="view_requirement_responses_view"
    ),
    path(
        "responses/<int:pk>/update-status/",
        UpdateRequirementResponseStatusView.as_view(),
        name="update_requirement_response_status_view"
    ),
    path(
        "<int:pk>/close/",
        CloseRequirementView.as_view(),
        name="close_requirement_view"
    ),
]