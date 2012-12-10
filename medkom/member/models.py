from django.db import models

YEAR_CHOICE = ()
for i in range(1950,2020):
    YEAR_ITEM = (i,i)
    YEAR_CHOICE += (YEAR_ITEM,)

class Family(models.Model):
    nomor_quesioner = models.CharField(max_length=6)
    nomor_kk = models.CharField(max_length=100)
    alamat_desa = models.ForeignKey('wilayah.Desa')
    alamat_dusun = models.ForeignKey('wilayah.Dusun')
    alamat_kampung = models.ForeignKey('wilayah.Kampung')
    alamat_rt = models.ForeignKey('wilayah.RT')
    status_rumah = models.ForeignKey('StatusRumah')
    lantai = models.ForeignKey('Lantai')
    dinding = models.ForeignKey('Dinding')
    atap = models.ForeignKey('Atap')
    penerima_jamsos = models.BooleanField()
    jamsos_diterima = models.ForeignKey('JamsosDiterima', blank=True, null=True)
    kepemilikan_wc = models.BooleanField()
    sumber_air_minum = models.ForeignKey('SumberAirMinum')
    status_listrik = models.ForeignKey('StatusListrik')
    daya_listrik = models.ForeignKey('DayaListrik', blank=True, null=True)
    jadwal_ronda = models.ForeignKey('JadwalRonda', blank=True, null=True)
    program_kb = models.ForeignKey('ProgramKB', blank=True, null=True)

    def __unicode__(self):
        return u'%s' %(self.nomor_kk)

class Person(models.Model):
    family = models.ForeignKey('Family')
    nama_lengkap = models.CharField(max_length=100)
    nama_panggilan = models.CharField(max_length=20, blank=True)
    nomor_nik = models.CharField(max_length=30, blank=True)
    tempat_lahir = models.CharField(max_length=50)
    tanggal_lahir = models.DateField()
    SEX = (
        (0, 'Laki Laki'),
        (1, 'Perempuan'),
    )
    jenis_kelamin = models.IntegerField(choices=SEX, default=0)
    agama = models.ForeignKey('Agama')
    status_ktp = models.BooleanField()
    domisili = models.CharField(max_length=50, blank=True)
    status_perkawinan = models.ForeignKey('StatusPerkawinan')
    hubungan_keluarga = models.ForeignKey('HubunganKeluarga')
    pendidikan_terakhir = models.ForeignKey('PendidikanTerakhir', blank=True, null=True)
    jurusan = models.ForeignKey('Jurusan', blank=True, null=True)
    tahun_lulus = models.IntegerField(choices=YEAR_CHOICE, null=True, blank=True)
    pekerjaan = models.ForeignKey('Pekerjaan', null=True, blank=True)
    no_handphone = models.CharField(max_length=15, blank=True)
    hobi = models.ManyToManyField('Hobi', blank=True, null=True)
    keahlian = models.ManyToManyField('Keahlian', blank=True, null=True)
    jenis_usaha = models.ManyToManyField('JenisUsaha', blank=True, null=True)
    penghasilan_bulanan = models.ForeignKey('PenghasilanBulanan', blank=True, null=True)
    organisasi = models.ManyToManyField('Organisasi', blank=True, null=True)
    media = models.ManyToManyField('Media', blank=True, null=True)
    tema_informasi = models.ManyToManyField('TemaInformasi', blank=True, null=True)
    alat_transportasi = models.ManyToManyField('AlatTransportasi', blank=True, null=True)

    pendonor_darah = models.BooleanField()
    golongan_darah = models.ForeignKey('GolonganDarah', blank=True, null=True)
    status_social_score = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u'%s' %(self.nama_lengkap)

# ===== Options ======
class Handphone(models.Model):
    person = models.ForeignKey('Person')
    nomor_handphone = models.CharField(max_length=15)
    status = models.BooleanField()

    def __unicode__(self):
        return u'%s' %(self.nomor_handphone)

class KeluargaGangguan(models.Model):
    family = models.ForeignKey('Family')
    jenis_difable = models.ForeignKey('JenisDifable')
    jumlah_difable = models.IntegerField()

    def __unicode__(self):
        return u'%s : %d' %(self.jenis_difable, self.jumlah_difable)

class JenisDifable(models.Model):
    jenis_difable = models.CharField(max_length=20)
    
    def __unicode__(self):
        return u'%s' %(self.jenis_difable)

class StatusRumah(models.Model):
    status_rumah = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s' %(self.status_rumah)

class Lantai(models.Model):
    lantai = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s' %(self.lantai)

class Dinding(models.Model):
    dinding = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s' %(self.dinding)

class Atap(models.Model):
    atap = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s' %(self.atap)

class JamsosDiterima(models.Model):
    jamsos_diterima = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' %(self.jamsos_diterima)

class SumberAirMinum(models.Model):
    sumber_air_minum = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' %(self.sumber_air_minum)

class StatusListrik(models.Model):
    status_listrik = models.CharField(max_length=15)

    def __unicode__(self):
        return u'%s' %(self.status_listrik)

class DayaListrik(models.Model):
    besar_daya = models.IntegerField()

    def __unicode__(self):
        return u'%d' %(self.besar_daya)

class JadwalRonda(models.Model):
    jadwal_ronda = models.CharField(max_length=7)

    def __unicode__(self):
        return u'%s' %(self.jadwal_ronda)

class ProgramKB(models.Model):
    program_kb = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' %(self.program_kb)

class Agama(models.Model):
    agama = models.CharField(max_length=30)
    
    def __unicode__(self):
        return u'%s' %(self.agama)

class StatusPerkawinan(models.Model):
    status_perkawinan = models.CharField(max_length=15)

    def __unicode__(self):
        return u'%s' %(self.status_perkawinan)

class HubunganKeluarga(models.Model):
    hubungan_keluarga = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s' %(self.hubungan_keluarga)

class PendidikanTerakhir(models.Model):
    pendidikan_terakhir = models.CharField(max_length=5)
    status_social_score = models.PositiveIntegerField()

    def __unicode__(self):
        return u'%s' %(self.pendidikan_terakhir)

class Jurusan(models.Model):
    jurusan = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' %(self.jurusan)

class Pekerjaan(models.Model):
    pekerjaan = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' %(self.pekerjaan)

class GolonganDarah(models.Model):
    golongan_darah = models.CharField(max_length=2)

    def __unicode__(self):
        return u'%s' %(self.golongan_darah)

class PenghasilanBulanan(models.Model):
    nilai_min = models.DecimalField(max_digits=10, decimal_places=2)
    nilai_max = models.DecimalField(max_digits=10, decimal_places=2)
    status_social_score = models.PositiveIntegerField()

    def __unicode__(self):
        return u'%d - %d' %(self.nilai_min, self.nilai_max)

# ====== Many to Many ======

class Hobi(models.Model):
    hobi = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' %(self.hobi)

class Keahlian(models.Model):
    keahlian = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' %(self.keahlian)

class JenisUsaha(models.Model):
    jenis_usaha = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' %(self.jenis_usaha)

class Organisasi(models.Model):
    organisasi = models.CharField(max_length=50)
    jabatan = models.CharField(max_length=50)
    
    def __unicode__(self):
        return u'%s | %s' %(self.organisasi, self.jabatan)

class Media(models.Model):
    media_yang_dipakai = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' %(self.media_yang_dipakai)

class TemaInformasi(models.Model):
    tema_informasi = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' %(self.tema_informasi)

class AlatTransportasi(models.Model):
    alat_transportasi = models.CharField(max_length=50)
    status_social_score = models.PositiveIntegerField()

    def __unicode__(self):
        return u'%s' %(self.alat_transportasi)

# ==== Parameter Sosial ====

class Usia(models.Model):
    name = models.CharField(max_length=15)
    umur_min = models.PositiveIntegerField()
    umur_max = models.PositiveIntegerField()
    
    def __unicode__(self):
        return u'%s (%s - %s)' %(self.name, self.umur_min, self.umur_max)
    
class StatusSosial(models.Model):
    name = models.CharField(max_length=15)
    score_min = models.PositiveIntegerField()
    score_max = models.PositiveIntegerField()
    
    def __unicode__(self):
        return u'%s' % self.name
    