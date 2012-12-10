from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from accounts.decorators import admin_required
from django.db.models import Q, F
from django.db import connection, transaction
from message.models import Queue, Log, Broadcast
from message.forms import (DeleteMessagesForm, BroadcastForm,
                           SettingBroadcastForm, ReplyForm, SearchForm)
from member.models import Person, Usia, StatusSosial
import datetime

@login_required
def home(request):
    if request.method == "POST":
        form = DeleteMessagesForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data["queue"] == '':
                list_messages = [x for x in form.cleaned_data["queue"].split(',')]
                messages = Queue.objects.filter(id__in=list_messages)
                messages.delete()
            
            return HttpResponseRedirect(reverse('home'))
    else:
        form = DeleteMessagesForm()
    
    queue_list = Queue.objects.filter(status__exact="1").order_by('-id')
    paginator = Paginator(queue_list, 5)
    page = request.GET.get('page')
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    
    return render_to_response('message/home.html',
                              {"messages": messages, "form": form, },
                              context_instance=RequestContext(request))

@login_required
def messages(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        queue_list = ''
        if form.is_valid():
            q = form.cleaned_data["q"]
            persons = Person.objects.exclude(no_handphone='').filter(nama_lengkap__icontains=q)
            queryset = Q()
            for person in persons:
                queryset.add(Q(
                    sender__icontains=person.no_handphone[1:]
                ), Q.OR)
            
            queryset.add(Q(
                message__icontains=q
            ), Q.OR)
            
            queue_list = Queue.objects.filter(queryset)
    else:
        form = SearchForm()
        queue_list = Queue.objects.all().order_by('-id')
        
    paginator = Paginator(queue_list, 5)
    page = request.GET.get('page')
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
        
    return render_to_response("message/messages.html",
                              {"messages": messages, "form":form, },
                              context_instance=RequestContext(request))

@login_required
def view_message(request, msg_id):
    queue = get_object_or_404(Queue, pk=msg_id)
    if request.method == 'POST':
        form = BroadcastForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            # Send to member
            if form.cleaned_data["member"]:
                queryset = _get_queryset(form)
                if queryset:
                    persons = Person.objects.filter(queryset)
                else:
                    persons = Person.objects.all()
                    
                _send_sms(persons, message)
                _write_log(persons, message, queue)
                
                # Modify message
                queue.status = 0 #processed
                queue.resolution = 0 #approved
                queue.save()
            
            if form.cleaned_data["external"]:
                if form.cleaned_data["extra_phones"]:
                    phones = form.cleaned_data["extra_phones"].split(',')
                    for phone in phones:
                        _send_single_sms(phone, message)
                        
            return HttpResponseRedirect(reverse('home'))
    else:
        form = BroadcastForm(initial={
            'message': queue.message
        })
    
    return render_to_response("message/view_message.html",
                              {"message": queue, "form": form, },
                              context_instance=RequestContext(request))

@login_required
def new_message(request):
    if request.method == 'POST':
        form = BroadcastForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            
            #Send Member
            if form.cleaned_data["member"]:
                queryset = _get_queryset(form)
                if queryset:
                    persons = Person.objects.filter(queryset)
                else:
                    persons = Person.objects.all()
                    
                _send_sms(persons, message)
                _write_log(persons, message)
            
            #Send External Receiver
            if form.cleaned_data["external"]:
                if form.cleaned_data["extra_phones"]:
                    phones = form.cleaned_data["extra_phones"].split(',')
                    for phone in phones:
                        _send_single_sms(phone, message)
            
            return HttpResponseRedirect(reverse('home'))
    else:
        form = BroadcastForm()
    
    return render_to_response("message/new_message.html",
                              {"form": form,},
                              context_instance=RequestContext(request))

@login_required
def decline(request, msg_id):
    if request.method == 'POST':
        queue = get_object_or_404(Queue, pk=request.POST.get('msg-id'))
        queue.status = 0
        queue.resolution = 1
        queue.save()
    
    return HttpResponseRedirect(reverse('home'))

@login_required
def delete(request, msg_id):
    if request.method =='POST':
        message = get_object_or_404(Queue, pk=request.POST.get('del-id'))
        message.delete()
    
    return HttpResponseRedirect(reverse('home'))

@admin_required
def broadcast(request):
    if request.method == "POST":
        form = SettingBroadcastForm(request.POST)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse('broadcast'))
    else:
        form = SettingBroadcastForm()
        
    broadcasts = Broadcast.objects.all()
    
    return render_to_response("message/broadcast.html",
                              {"broadcasts": broadcasts, "form":form,},
                              context_instance=RequestContext(request))

@admin_required
def view_broadcast(request, b_id):
    broadcast = get_object_or_404(Broadcast, pk=b_id)
    if request.method == "POST":
        form = SettingBroadcastForm(request.POST, instance=broadcast)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse('broadcast'))
    else:
        form = SettingBroadcastForm(instance=broadcast)
        
    return render_to_response("message/view_broadcast.html",
                              {"broadcast":broadcast, "form":form,},
                              context_instance=RequestContext(request))

@admin_required
def delete_broadcast(request, b_id):
    if request.method == "POST":
        broadcast = get_object_or_404(Broadcast, pk=request.POST.get('b-id'))
        broadcast.delete()
        
    return HttpResponseRedirect(reverse('broadcast'))

@login_required
def archive(request):
    log_list = Log.objects.all().order_by('-id')
    paginator = Paginator(log_list, 10)
    page = request.GET.get('page')
    
    try:
        archives = paginator.page(page)
    except PageNotAnInteger:
        archives = paginator.page(1)
    except EmptyPage:
        archives = paginator.page(paginator.num_pages)
        
    return render_to_response(
        "message/archive.html",
        {"archives": archives, },
        context_instance=RequestContext(request)
    )

@login_required
def log(request):
    items = _fetch_sentitems()
    paginator = Paginator(items, 10)
    page = request.GET.get('page')
    try:
        sentitems = paginator.page(page)
    except PageNotAnInteger:
        sentitems = paginator.page(1)
    except EmptyPage:
        sentitems = paginator.page(paginator.num_pages)
    
    return render_to_response(
        "message/log.html",
        {"sentitems":sentitems,},
        context_instance=RequestContext(request)
    )

@login_required
def reply(request, msg_id):
    msg = get_object_or_404(Queue, pk=msg_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            destination = form.cleaned_data["destination"]
            _send_single_sms(destination, message)
            _write_single_log(message)
            
            # Modify message
            msg.status = 0 #processed
            msg.resolution = 0 #approved
            msg.save()
            
            return HttpResponseRedirect(reverse('home'))
    else:
        form = ReplyForm(
            initial={'destination': msg.sender}
        )
    
    return render_to_response("message/reply.html",
                              {"msg": msg, "form": form, },
                              context_instance=RequestContext(request))

@login_required
def new_single_message(request, no_hp):
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            destination = form.cleaned_data["destination"]
            _send_single_sms(destination, message)
            _write_single_log(message)
            
            return HttpResponseRedirect(reverse('home'))
    else:
        form = ReplyForm(
            initial={'destination': no_hp}
        )
        
    return render_to_response('message/new_single_message.html',
                              {"form":form, "destination":no_hp,},
                              context_instance=RequestContext(request))

def _get_queryset(form):
    """
    Choices is :
    REL_CHOICES = (
        (0, "Dan"),
        (1, "Atau"),
    )
    """
    queryset = Q()
    if form.cleaned_data["tema_informasi"]:
        if form.cleaned_data["tema_informasi_rel"] == '1':
            queryset.add(Q(
                tema_informasi__in=form.cleaned_data["tema_informasi"]
            ), Q.OR)
        else:
            queryset.add(Q(
                tema_informasi__in=form.cleaned_data["tema_informasi"]
            ), Q.AND)
    
    if form.cleaned_data["hubungan_keluarga"]:
        if form.cleaned_data["hubungan_keluarga_rel"] == '1':
            queryset.add(Q(
                hubungan_keluarga__in=form.cleaned_data["hubungan_keluarga"]
            ), Q.OR)
        else:
            queryset.add(Q(
                hubungan_keluarga__in=form.cleaned_data["hubungan_keluarga"]
            ), Q.AND)
            
    if form.cleaned_data["jenis_kelamin"]:
        if form.cleaned_data["jenis_kelamin_rel"] == '1':
            queryset.add(Q(
                jenis_kelamin__in=form.cleaned_data["jenis_kelamin"]
            ), Q.OR)
        else:
            queryset.add(Q(
                jenis_kelamin__in=form.cleaned_data["jenis_kelamin"]
            ), Q.AND)
            
    if form.cleaned_data["domisili"]:
        if form.cleaned_data["domisili_rel"] == '1':
            queryset.add(Q(
                domisili__in=form.cleaned_data["domisili"]
            ), Q.OR)
        else:
            queryset.add(Q(
                domisili__in=form.cleaned_data["domisili"]
            ), Q.AND)
            
    if form.cleaned_data["agama"]:
        if form.cleaned_data["agama_rel"] == '1':
            queryset.add(Q(
                agama__in=form.cleaned_data["agama"]
            ), Q.OR)
        else:
            queryset.add(Q(
                agama__in=form.cleaned_data["agama"]
            ), Q.AND)
            
    if form.cleaned_data["organisasi"]:
        if form.cleaned_data["organisasi_rel"] == '1':
            queryset.add(Q(
                organisasi__in=form.cleaned_data["organisasi"]
            ), Q.OR)
        else:
            queryset.add(Q(
                organisasi__in=form.cleaned_data["organisasi"]
            ), Q.AND)
            
    if form.cleaned_data["jenis_usaha"]:
        if form.cleaned_data["jenis_usaha_rel"] == '1':
            queryset.add(Q(
                jenis_usaha__in=form.cleaned_data["jenis_usaha"]
            ), Q.OR)
        else:
            queryset.add(Q(
                jenis_usaha__in=form.cleaned_data["jenis_usaha"]
            ), Q.AND)
            
    if form.cleaned_data["keahlian"]:
        if form.cleaned_data["keahlian_rel"] == '1':
            queryset.add(Q(
                keahlian__in=form.cleaned_data["keahlian"]
            ), Q.OR)
        else:
            queryset.add(Q(
                keahlian__in=form.cleaned_data["keahlian"]
            ),Q.OR)
            
    if form.cleaned_data["pendidikan_terakhir"]:
        if form.cleaned_data["pendidikan_terakhir_rel"] == '1':
            queryset.add(Q(
                pendidikan_terakhir__in=form.cleaned_data["pendidikan_terakhir"]
            ), Q.OR)
        else:
            queryset.add(Q(
                pendidikan_terakhir__in=form.cleaned_data["pendidikan_terakhir"]
            ), Q.AND)
            
    if form.cleaned_data["jurusan"]:
        if form.cleaned_data["jurusan_rel"] == '1':
            queryset.add(Q(
                jurusan__in=form.cleaned_data["jurusan"]
            ), Q.OR)
        else:
            queryset.add(Q(
                jurusan__in=form.cleaned_data["jurusan"]
            ), Q.AND)
            
    if form.cleaned_data["pekerjaan"]:
        if form.cleaned_data["pekerjaan_rel"] == '1':
            queryset.add(Q(
                pekerjaan__in=form.cleaned_data["pekerjaan"]
            ), Q.OR)
        else:
            queryset.add(Q(
                pekerjaan__in=form.cleaned_data["pekerjaan"]
            ), Q.AND)
            
    if form.cleaned_data["penerima_jaminan_sosial"]:
        if form.cleaned_data["penerima_jaminan_sosial_rel"] == '1':
            queryset.add(Q(
                family__penerima_jamsos__in=form.cleaned_data[
                    "penerima_jaminan_sosial"
                ]
            ), Q.OR)
        else:
            queryset.add(Q(
                family__penerima_jamsos__in=form.cleaned_data[
                    "penerima_jaminan_sosial"
                ]
            ), Q.AND)
            
    if form.cleaned_data["golongan_darah"]:
        if form.cleaned_data["golongan_darah_rel"] == '1':
            queryset.add(Q(
                golongan_darah__in=form.cleaned_data["golongan_darah"]
            ), Q.OR)
        else:
            queryset.add(Q(
                golongan_darah__in=form.cleaned_data["golongan_darah"]
            ), Q.AND)
            
    if form.cleaned_data["jadwal_ronda"]:
        if form.cleaned_data["jadwal_ronda_rel"] == '1':
            queryset.add(Q(
                family__jadwal_ronda__in=form.cleaned_data["jadwal_ronda"]
            ), Q.OR)
        else:
            queryset.add(Q(
                family__jadwal_ronda__in=form.cleaned_data["jadwal_ronda"]
            ), Q.AND)
            
    # Usia - Status Sosial
    if form.cleaned_data["usia"]:
        age = _get_age(form.cleaned_data["usia"])
        
        if form.cleaned_data["usia_rel"] == '1':
            queryset.add(Q(
                tanggal_lahir__range=(age[0],age[1])
            ), Q.OR)
        else:
            queryset.add(Q(
                tanggal_lahir__range=(age[0],age[1])
            ), Q.AND)
            
    if form.cleaned_data["status_sosial"]:
        statuses = form.cleaned_data["status_sosial"]
        status_min = []
        status_max = []
        for status in statuses:
            status_min.append(status.score_min)
            status_max.append(status.score_max)
            
        score_min = min(status_min)
        score_max = max(status_max)
        
        if form.cleaned_data["status_sosial_rel"] == '1':
            queryset.add(Q(
                status_social_score__range=(score_min,score_max)
            ), Q.OR)
        else:
            queryset.add(Q(
                status_social_score__range=(score_min,score_max)
            ), Q.AND)
            
    # Wilayah 
    if form.cleaned_data["desa"]:
        if form.cleaned_data["wilayah_rel"] == '1':
            queryset.add(Q(
                family__alamat_desa__in=form.cleaned_data["desa"]
            ), Q.OR)
        else:
            queryset.add(Q(
                family__alamat_desa__in=form.cleaned_data["desa"]
            ), Q.AND)
            
    if form.cleaned_data["dusun"]:
        if form.cleaned_data["wilayah_rel"] == '1':
            queryset.add(Q(
                family__alamat_dusun__in=form.cleaned_data["dusun"]
            ), Q.OR)
        else:
            queryset.add(Q(
                family__alamat_dusun__in=form.cleaned_data["dusun"]
            ), Q.AND)
            
    if form.cleaned_data["kampung"]:
        if form.cleaned_data["wilayah_rel"] == '1':
            queryset.add(Q(
                family__alamat_kampung__in=form.cleaned_data["kampung"]
            ), Q.OR)
        else:
            queryset.add(Q(
                family__alamat_kampung__in=form.cleaned_data["kampung"]
            ), Q.AND)
            
    if form.cleaned_data["rt"]:
        if form.cleaned_data["wilayah_rel"] == '1':
            queryset.add(Q(
                family__alamat_rt__in=form.cleaned_data["rt"]
            ), Q.OR)
        else:
            queryset.add(Q(
                family__alamat_rt__in=form.cleaned_data["rt"]
            ), Q.AND)
            
    return queryset

def _get_age(ages):
    day_in_a_year = 365
    age_min = []
    age_max = []
    
    for age in ages:
        age_min.append(age.umur_min)
        age_max.append(age.umur_max)
    
    min_age = min(age_min)
    max_age = max(age_max)
    
    date_start = datetime.date.today() - datetime.timedelta(
        max_age * day_in_a_year
    )
    date_finish = datetime.date.today() - datetime.timedelta(
        min_age * day_in_a_year
    )
    result = [date_start,date_finish]
    
    return result

def _send_sms(persons, message):
    cursor = connection.cursor()
    for person in persons:
        if person.no_handphone != '':
            cursor.execute(
                "INSERT INTO outbox(DestinationNumber,Coding,TextDecoded,CreatorID) \
                  VALUES(%s,'Default_No_Compression',%s,'1')",
                [person.no_handphone,message]
            )
        
    transaction.commit_unless_managed()

def _send_single_sms(destination, message):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO outbox(DestinationNumber,Coding,TextDecoded,CreatorID) \
          VALUES(%s,'Default_No_Compression',%s,'1')",
        [destination,message]
    )
    transaction.commit_unless_managed()

def _write_log(persons, message, msg_id=None):
    log = Log()
    log.message = message
    log.date = timezone.localtime(timezone.now())
    if msg_id:
        log.queue = msg_id
    
    log.save()
    for person in persons:
        log.persons.add(person)

def _write_single_log(message, msg_id=None, person=None):
    log = Log()
    log.message = message
    log.date = timezone.localtime(timezone.now())
    if msg_id:
        log.queue = msg_id
    
    log.save()
    if person:
        log.persons.add(person)
    
def _fetch_sentitems():
    cursor = connection.cursor()
    cursor.execute("SELECT SendingDateTime,DestinationNumber,\
                   TextDecoded,Status FROM sentitems order by ID DESC")
    
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

