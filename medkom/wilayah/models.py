from django.db import models

class Desa(models.Model):
    nama_desa = models.CharField(max_length=20)
    
    def __unicode__(self):
        return u'%s' % (self.nama_desa)

class Dusun(models.Model):
    nama_desa = models.ForeignKey('Desa')
    nama_dusun = models.CharField(max_length=20)
    
    def __unicode__(self):
        return u'%s' % self.nama_dusun

class Kampung(models.Model):
    nama_dusun = models.ForeignKey('Dusun')
    nama_kampung = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s (%s)' % (self.nama_kampung, self.nama_dusun)

class RT(models.Model):
    nama_rt = models.IntegerField()

    def __unicode__(self):
        return u'%d' % (self.nama_rt)

