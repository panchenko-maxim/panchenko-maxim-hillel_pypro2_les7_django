from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

User = get_user_model()


@login_required()
@permission_required('accounts.can_view_profiles', '')
def restricted_page(request):
    # if not request.user.has_perm('accounts.can_view_profiles'):
    return render(request, 'permissions/restricted_page.html', {'user', request.user})


@login_required()
def su_only(request):
    if not request.user.is_superuser:
        messages.error(request, "Only for superusers")

    return render(request, 'permissions/su_page.html', {'user': request.user})

@login_required()
def list_users(request):
    if not request.user.is_superuser:
        messages.error(request, "Only for superusers")
        return redirect('home')

    users = User.objects.all().exclude(id=request.user.id)
    return redirect(request,'permissions/user_list.html', {'users': users})

@login_required()
def manage_permissions(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Only for superusers")
        return redirect('home')
    user = get_object_or_404(User, id = user_id)


