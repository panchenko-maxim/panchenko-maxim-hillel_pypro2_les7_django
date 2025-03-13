from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from django.contrib import messages


@login_required()
@permission_required('accounts.can_view_profiles', '')
def restricted_page(request):
    # if not request.user.has_perm('accounts.can_view_profiles'):
    return render(request, 'permissions/restricted_page.html', {'user', request.user})


@login_required()
def su_only(request):
    if not request.user.is_superuser:
        messages.error(request, "Only for superusers")


