from member.models import *
from django.contrib import admin
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import CheckboxSelectMultiple
from django.forms import Select

class PersonInline(admin.StackedInline):
    model = Person
    extra = 1
    formfield_overrides = {
        models.DateField: {'widget': SelectDateWidget(years=range(1950,2020))},
        models.ManyToManyField: {'widget': CheckboxSelectMultiple()},
    }
    
    fieldsets = (
        (None, {
            'fields': (
            ('hubungan_keluarga', 'pekerjaan', 'no_handphone'),
            ('nama_lengkap','nama_panggilan'),
            ('nomor_nik', 'domisili', 'status_ktp'),
            ('tempat_lahir', 'tanggal_lahir'),
            ('jenis_kelamin', 'agama', 'status_perkawinan'),
            ('pendidikan_terakhir', 'jurusan', 'tahun_lulus'),
            'penghasilan_bulanan',
            ('hobi', 'keahlian'),
            ('jenis_usaha'),
            ('organisasi', 'media'),
            ('tema_informasi', 'alat_transportasi'),
            ('golongan_darah', 'pendonor_darah'),
            ),
        }),
    )

class HandphoneInline(admin.StackedInline):
    model = Handphone

class PersonAdmin(admin.ModelAdmin):
    inlines = [HandphoneInline]

class KeluargaGangguanInline(admin.StackedInline):
    model = KeluargaGangguan
    extra = 1
    fieldsets = (
        (None, {
            'fields': (('jenis_difable', 'jumlah_difable'),),
        }),
    )

class FamilyAdmin(admin.ModelAdmin):
    list_display = ('nomor_quesioner', 'nomor_kk', 'alamat_desa', 'alamat_dusun', 'alamat_kampung')
    list_filter = ('status_rumah', 'lantai', 'alamat_desa', 'alamat_dusun')
    list_per_page = 20
    search_fields = ['nomor_kk', 'nomor_quesioner']
    fieldsets = (
        (None, {
            'fields': (
            ('nomor_quesioner', 'nomor_kk'),
            ('alamat_desa', 'alamat_dusun', 'alamat_kampung', 'alamat_rt'),
            ('status_rumah', 'lantai', 'dinding', 'atap'),
            ('penerima_jamsos', 'jamsos_diterima'),
            ('kepemilikan_wc', 'sumber_air_minum'),
            ('status_listrik', 'daya_listrik'),
            ('jadwal_ronda', 'program_kb'),
            ),
        }),
    )
    
    inlines = [KeluargaGangguanInline,PersonInline]

# ====== Options =======

class JenisDifableAdmin(admin.ModelAdmin):
    pass

class StatusRumahAdmin(admin.ModelAdmin):
    pass
    
class LantaiAdmin(admin.ModelAdmin):
    pass

class DindingAdmin(admin.ModelAdmin):
    pass

class AtapAdmin(admin.ModelAdmin):
    pass

class JamsosDiterimaAdmin(admin.ModelAdmin):
    pass

class SumberAirMinumAdmin(admin.ModelAdmin):
    pass

class StatusListrikAdmin(admin.ModelAdmin):
    pass

class DayaListrikAdmin(admin.ModelAdmin):
    pass

class JadwalRondaAdmin(admin.ModelAdmin):
    pass

class ProgramKBAdmin(admin.ModelAdmin):
    pass

class AgamaAdmin(admin.ModelAdmin):
    pass

class StatusPerkawinanAdmin(admin.ModelAdmin):
    pass

class HubunganKeluargaAdmin(admin.ModelAdmin):
    pass

class PendidikanTerakhirAdmin(admin.ModelAdmin):
    pass

class JurusanAdmin(admin.ModelAdmin):
    pass

class PekerjaanAdmin(admin.ModelAdmin):
    pass

class GolonganDarahAdmin(admin.ModelAdmin):
    pass

## === Many to many ===
class HobiAdmin(admin.ModelAdmin):
    pass

class KeahlianAdmin(admin.ModelAdmin):
    pass

class JenisUsahaAdmin(admin.ModelAdmin):
    pass

class PenghasilanBulananAdmin(admin.ModelAdmin):
    pass

class OrganisasiAdmin(admin.ModelAdmin):
    list_display = ('organisasi', 'jabatan')

class MediaAdmin(admin.ModelAdmin):
    pass

class TemaInformasiAdmin(admin.ModelAdmin):
    pass

class AlatTransportasiAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Family, FamilyAdmin)
admin.site.register(Person, PersonAdmin)

admin.site.register(JenisDifable, JenisDifableAdmin)
admin.site.register(StatusRumah, StatusRumahAdmin)
admin.site.register(Lantai, LantaiAdmin)
admin.site.register(Dinding, DindingAdmin)
admin.site.register(Atap, AtapAdmin)
admin.site.register(JamsosDiterima, JamsosDiterimaAdmin)
admin.site.register(SumberAirMinum, SumberAirMinumAdmin)
admin.site.register(StatusListrik, StatusListrikAdmin)
admin.site.register(DayaListrik, DayaListrikAdmin)
admin.site.register(JadwalRonda, JadwalRondaAdmin)
admin.site.register(ProgramKB, ProgramKBAdmin)
admin.site.register(Agama, AgamaAdmin)
admin.site.register(StatusPerkawinan, StatusPerkawinanAdmin)
admin.site.register(HubunganKeluarga, HubunganKeluargaAdmin)
admin.site.register(PendidikanTerakhir, PendidikanTerakhirAdmin)
admin.site.register(Jurusan, JurusanAdmin)
admin.site.register(Pekerjaan, PekerjaanAdmin)
admin.site.register(GolonganDarah, GolonganDarahAdmin)

admin.site.register(Hobi, HobiAdmin)
admin.site.register(Keahlian, KeahlianAdmin)
admin.site.register(JenisUsaha, JenisUsahaAdmin)
admin.site.register(PenghasilanBulanan, PenghasilanBulananAdmin)
admin.site.register(Organisasi, OrganisasiAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(TemaInformasi, TemaInformasiAdmin)
admin.site.register(AlatTransportasi, AlatTransportasiAdmin)

