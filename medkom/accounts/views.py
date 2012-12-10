from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from accounts.forms import NewUserForm, EditUserForm

@admin_required
def admin(request):
    select = request.GET.get('q', 'all')
    users = {
        "all" : lambda : User.objects.all().order_by('-id'),
        "active" : lambda : User.objects.filter(is_active=True).order_by('-id'),
        "inactive" : lambda : User.objects.filter(is_active=False).order_by('-id'),
        "admin" : lambda : User.objects.filter(is_superuser=True).order_by('-id'),
        "staff" : lambda : User.objects.filter(is_staff=True,
                                            is_superuser=False).order_by('-id'),
        "user" : lambda : User.objects.filter(is_active=True,
                            is_superuser=False, is_staff=False).order_by('-id')
    }.get(select, lambda : User.objects.all().order_by('-id'))()

    return render_to_response("accounts/admin.html",
                            {"users": users, },
                            context_instance=RequestContext(request))

@admin_required
def view_account(request, user_id):
    try:
        view_user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        raise Http404
    
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=view_user)
        if form.is_valid():
            form.save()
    else:
        form = EditUserForm(instance=view_user)
    
    return render_to_response("accounts/view.html",
                                {"view_user": view_user, "form": form,},
                                context_instance=RequestContext(request))

@admin_required
def delete_account(request, user_id):
    if request.method == "POST":
        try:
            delete_user = User.objects.get(pk=request.POST.get('user-id'))
            delete_user.is_active = False
            delete_user.save()
        except ObjectDoesNotExist:
            raise Http404

    return HttpResponseRedirect('../../')

@admin_required
def change_password(request, user_id):
    try:
        passwd_user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        raise Http404
    
    if request.method == "POST":
        form = AdminPasswordChangeForm(passwd_user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../../')
    
    else:
        form = AdminPasswordChangeForm(passwd_user)
    
    return render_to_response("accounts/admin_passwd.html",
                                {"form": form, "passwd_user": passwd_user},
                                context_instance=RequestContext(request))

@admin_required
def new(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("../")
    else:
        form = NewUserForm()

    return render_to_response("accounts/new.html",
                            {"form": form,},
                            context_instance=RequestContext(request))

@login_required
def profile(request):
    return render_to_response("accounts/profile.html",
                              {},
                              context_instance=RequestContext(request))
