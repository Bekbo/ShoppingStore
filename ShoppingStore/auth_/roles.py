from rest_framework.permissions import BasePermission


class SellerPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_seller)


class CustomerPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_customer)
