from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.account.role.role_name == 'Admin'

class PostOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, post):
        if view.action == 'destroy':
            return request.user == post.account.user \
                   or request.user.account.role.role_name == 'Admin'
        elif view.action in ['update', 'partial_update']:
            return request.user == post.account.user

class PostOwnerAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, post):
        return request.user == post.account.user

class CanManageScorePermission(permissions.BasePermission):
    """
    Quyền hạn cho phép người dùng quản lý điểm.
    """
    message = "You do not have permission to manage score."

    def has_permission(self, request, view):
        return request.user.has_perm('courseapp.can_manage_score')

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Teacher').exists()
