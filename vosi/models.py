# -*- coding: utf-8 -*-

from django.db import models

ACCESS_URL_USE_CHOICES = (
    ('full', 'full'),
    ('base', 'base'),
    ('dir', 'dir'),
)

class AvailabilityOption(models.Model):
    id = models.IntegerField(primary_key=True)
    available = models.BooleanField(help_text="True if the service is available, else false")
    note = models.CharField(max_length=256, blank=True, null=True, help_text="A status message")
    #upSince =
    #downAt =
    #backAt =
    #enabled = models.BooleanField(help_text="Indicate if this status active or not")
    appname = models.CharField(max_length=128, blank=True, null=True)  # used to serve only a subset of capabilities for sub-apps

class Availability(models.Model):
    enabled = models.ForeignKey(AvailabilityOption, on_delete=models.CASCADE)
    appname = models.CharField(max_length=128, blank=True, null=True)  # used to serve only a subset of capabilities for sub-apps


class VOResource_Capability(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=256, blank=True, null=True)  # use choices?
    standardID = models.CharField(max_length=256, blank=True, null=True)  # use choices?
    description = models.CharField(max_length=1024, blank=True, null=True)
    # validationLevel [0..*] -- ignore here
    appname = models.CharField(max_length=128, blank=True, null=True)  # used to serve only a subset of capabilities for sub-apps


class VOResource_Interface(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=256, default="vr:WebBrowser")  # use predefined choices here?
    capability = models.ForeignKey(VOResource_Capability, on_delete=models.CASCADE)
    version = models.CharField(max_length=256, blank=True, null=True, default="1.0")
    role = models.CharField(max_length=1024, blank=True, null=True)  # use choices?
    # securityMethod [0..*] -- ignore here


class VOResource_AccessURL(models.Model):
    id = models.AutoField(primary_key=True)
    interface = models.ForeignKey(VOResource_Interface, on_delete=models.CASCADE)
    url = models.CharField(max_length=1024)
    use = models.CharField(max_length=256, default="full", choices=ACCESS_URL_USE_CHOICES)
