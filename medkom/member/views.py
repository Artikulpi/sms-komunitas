from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.decorators import admin_required
from member.models import Usia, StatusSosial, Person
from member.forms import AgeForm, StatusSosialForm, SearchForm

@login_required
def home(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        person_list = ''
        if form.is_valid():
            q = form.cleaned_data["q"]
            person_list = Person.objects.filter(nama_lengkap__contains=q)
    else:
        form = SearchForm()
        person_list = Person.objects.all()
        
    paginator = Paginator(person_list, 5)
    page = request.GET.get('page')
    try:
        persons = paginator.page(page)
    except PageNotAnInteger:
        persons = paginator.page(1)
    except EmptyPage:
        persons = paginator.page(paginator.num_pages)
        
    return render_to_response('member/member.html',
                              {"persons":persons, "form":form,},
                              context_instance=RequestContext(request))

@login_required
def view_member(request,member_id):
    person = get_object_or_404(Person, pk=member_id)
    
    return render_to_response("member/view_member.html",
                              {"person":person, },
                              context_instance=RequestContext(request))

@admin_required
def settings_age(request):
    if request.method == 'POST':
        form = AgeForm(request.POST)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse('setting_age'))
    else:
        form = AgeForm()
        
    ages = Usia.objects.all()
    
    return render_to_response('member/settings_age.html',
                              {"ages": ages, "form": form, },
                              context_instance=RequestContext(request))

@admin_required
def view_age(request, age_id):
    age = get_object_or_404(Usia, pk=age_id)
    if request.method == "POST":
        form = AgeForm(request.POST, instance=age)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse('setting_age'))
    else:
        form = AgeForm(instance=age)
        
    return render_to_response("member/view_age.html",
                              {"age": age, "form": form, },
                              context_instance=RequestContext(request))

@admin_required
def delete_age(request, age_id):
    if request.method == 'POST':
        age = get_object_or_404(Usia, pk=request.POST.get("age-id"))
        age.delete()
        
    return HttpResponseRedirect(reverse('setting_age'))

@admin_required
def settings_social(request):
    if request.method == 'POST':
        form = StatusSosialForm(request.POST)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse('setting_social'))
    else:
        form = StatusSosialForm()
        
    statuses = StatusSosial.objects.all()
    
    return render_to_response('member/settings_social.html',
                              {"statuses": statuses, "form": form,},
                              context_instance=RequestContext(request))

@admin_required
def view_social(request, sos_id):
    social = get_object_or_404(StatusSosial, pk=sos_id)
    
    if request.method == 'POST':
        form = StatusSosialForm(request.POST, instance=social)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse('setting_social'))
    else:
        form = StatusSosialForm(instance=social)
        
    return render_to_response("member/view_social.html",
                              {"social": social, "form": form, },
                              context_instance=RequestContext(request))

@admin_required
def delete_social(request, sos_id):
    if request.method == 'POST':
        soc = get_object_or_404(StatusSosial, pk=request.POST.get('sos-id'))
        soc.delete()
        
    return HttpResponseRedirect(reverse('setting_social'))
