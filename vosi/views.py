# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from .renderers import VosiAvailabilityRenderer, VosiCapabilityRenderer
from .models import VOResource_Capability, Availability, AvailabilityOption

def availability(request):
    # should perform checks here, if databases are still reachable etc.
    # should write to db the status and note, uTDate etc. via admin interface as well

    # get availability from database; maybe an admin took the service down or so
    appname = request.resolver_match.app_name
    if appname == 'vosi':
        data = {'available': 'true', 'note': 'Service is ready for requests'}
    else:
        try:
            data = AvailabilityOption.objects.get(id=Availability.objects.get(appname=appname).enabled.id)
        except Exception as e:
            return HttpResponseServerError('Server Error: the server is down or the availability is not set properly. (%s)' % e)  # 500

        data = {'available': str(data.available).lower(), 'note': data.note}


    # do some performance tests here
    # set availability to False, if needed
    # try:
    #     ...
    # except Exception as e:
    #     data = {'available': 'false', 'note': 'Database cannot be queried.'}


    # return availability
    return HttpResponse(VosiAvailabilityRenderer().render(data), content_type="application/xml")


def capabilities(request):

    appname = request.resolver_match.app_name
    if appname == 'vosi':
        # return them all!
        capabilities = VOResource_Capability.objects.order_by('id')
    else:
        capabilities = VOResource_Capability.objects.filter(appname=appname).order_by('id')
    # now join them together -> do it in renderer (not efficient, but ok for now)

    vosicap = VosiCapabilityRenderer().render(capabilities)
    # response = HttpResponse(vosicap, content_type="text/xml")
    response = HttpResponse(vosicap, content_type="application/xml")
    return response

