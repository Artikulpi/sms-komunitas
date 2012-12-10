from django.db import models
from member.models import Person

class Queue(models.Model):
    date = models.DateTimeField()
    sender = models.CharField(max_length=20)
    message = models.CharField(max_length=200)
    MSG_STATUS = (
        (0, 'Moderated'),
        (1, 'Pending'),
    )
    status = models.IntegerField(choices=MSG_STATUS, default=0)
    
    MSG_RESOLUTION = (
        (0, 'Approved'),
        (1, 'Decline'),
    )
    resolution = models.IntegerField(choices=MSG_RESOLUTION, null=True)
    
    def __unicode__(self):
        return u'%s' %(self.id)

class Broadcast(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    def __unicode__(self):
        return u'%s : %s' %(self.name,self.phone)

class Log(models.Model):
    date = models.DateTimeField()
    message = models.CharField(max_length=200)
    persons = models.ManyToManyField(Person)
    queue = models.ForeignKey(Queue, null=True, blank=True)
    
    def __unicode__(self):
        return u'%s' % self.message
    
    