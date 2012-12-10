from django.contrib import admin
from wilayah.models import *

class DusunInline(admin.StackedInline):
    model = Dusun
    extra = 5

class KampungInline(admin.StackedInline):
    model = Kampung
    extra = 5

class DesaAdmin(admin.ModelAdmin):
    inlines = [DusunInline]

class DusunAdmin(admin.ModelAdmin):
    list_display = ('nama_dusun', 'nama_desa')
    inlines = [KampungInline]

class RTAdmin(admin.ModelAdmin):
    pass

admin.site.register(Desa, DesaAdmin)
admin.site.register(Dusun, DusunAdmin)
admin.site.register(RT, RTAdmin)

