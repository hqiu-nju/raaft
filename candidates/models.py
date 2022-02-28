from django.db import models
from django.utils import timezone

# Create your models here.

class TransientEntry(models.Model):
    """Recording an entry from a detection pipeline.
    Parameters
    ----------
    name : str
        Entry name of transient
    pub_date : DateTimeField
        Entry Date of this object
    beam : int
        Beam for multibeam receivers
    """
    # pipeline reported info should be going in here
    # S/N, sampno, secs from file start, boxcar, idt, dm, beamno, mjd, latency_ms
    # S/N, sampno, secs from file start, boxcar, idt, dm, beamno, mjd, latency_ms
    name = models.CharField(max_length=20)
    pub_date = models.DateTimeField('Publish Date',default=timezone.now)
    beam = models.IntegerField("Trigger Beam")
    dm = models.FloatField("DM")
    sn = models.FloatField("SNR")
    boxcar = models.IntegerField("Boxcar")
    width_value = models.FloatField("Pulse Width (ms)")
    mjd = models.FloatField("MJD")
    latency_ms = models.FloatField("Latency(ms)")
    # centre_frequency=models.FloatField("Frequency (MHz)",blank=True)
    ra = models.FloatField('Right Asension',blank=True)
    dec = models.FloatField("Declination",blank=True)
    #RA= models.FloatField("MJD")
    ## link latest verification
    def __str__(self):
        return self.name

class Properties(models.Model):
    frb = models.ForeignKey(TransientEntry, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Publish Date',default=timezone.now)
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return str(self.frb)+"_props"

class Veto(models.Model):
    frb = models.ForeignKey(TransientEntry, on_delete=models.CASCADE)
    verify=[
    (0,"Unverified"),
    (1,'FRB'),
    (2,'Pulsar'),
    (-1,'RFI'),
    (3,'Unknown')
    ]
    verify = models.CharField(choices=verify,default=0,max_length=20)
    reason=models.CharField(default="",max_length=200)
    pub_date = models.DateTimeField('date published',default=timezone.now)
    username=models.CharField(default='Anonymous',max_length=20)
    def __str__(self):
        return str(self.frb)+str('_Veto')

class Multimessenger(models.Model):
    frb = models.ForeignKey(TransientEntry, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published',default=timezone.now)
    choice_text = models.CharField('Info',max_length=200)
    username=models.CharField(default='Anonymous',max_length=20)
    ra = models.FloatField('Right Asension',blank=True)
    dec = models.FloatField("Declination",blank=True)
    ra_err = models.FloatField('RA err',blank=True)
    dec_err = models.FloatField('Dec err',blank=True)
    upload = models.FileField('Uploaded File',upload_to='uploads/',blank=True)
    def __str__(self):
        return str(self.frb)+"_multimessenger"
