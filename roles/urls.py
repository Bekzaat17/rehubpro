# roles/urls.py
from django.urls import path
from .views.assign_roles import AssignRolesView
from .views.manage_roles import ManageRolesView, ManageRolesApiView
from .views.resident_role_modal import ResidentRoleModalView

app_name = "roles"

urlpatterns = [
    path("assign/", AssignRolesView.as_view(), name="assign_roles"),
    path("resident/<int:resident_id>/modal/", ResidentRoleModalView.as_view(), name="resident-role-modal"),
    path("manage/", ManageRolesView.as_view(), name="manage_roles"),
    path("manage/api/", ManageRolesApiView.as_view(), name="role_create"),
    path("manage/api/<uuid:pk>/", ManageRolesApiView.as_view(), name="role_update_delete"),
]