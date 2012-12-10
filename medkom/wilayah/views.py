from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.core import serializers
from wilayah.models import Dusun, Kampung, RT

@login_required
def xhr_dusun(request, id_desa):
    if request.is_ajax():
        queryset = Dusun.objects.filter(nama_desa=id_desa)
        results = serializers.serialize('json', queryset)
        
        return HttpResponse(results, mimetype="application/javascript")
    else:
        return HttpResponse(status=400)

@login_required
def xhr_kampung(request, id_dusun):
    if request.is_ajax():
        queryset = Kampung.objects.filter(nama_dusun=id_dusun)
        results = serializers.serialize('json', queryset)
        
        return HttpResponse(results, mimetype="application/javascript")
    else:
        return HttpResponse(status=400)
