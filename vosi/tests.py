# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client
from django.test.utils import setup_test_environment

from vosi.models import Availability, AvailabilityOption
from vosi.models import VOResource_Capability, VOResource_Interface, VOResource_AccessURL


class Vosi_TestCase(TestCase):
    def setUp(self):
        ao_up = AvailabilityOption.objects.create(id="1", available=True, note="service is up", appname="example_app")
        ao_up.save()

        ao_down = AvailabilityOption.objects.create(id="2", available=False, note="service is down", appname="example_app")
        ao_down.save()

        a = Availability.objects.create(enabled=ao_up, appname="example_app")
        a.save()

        ao_up = AvailabilityOption.objects.create(id="3", available=True, note="service is up", appname="example2_app")
        ao_up.save()

        ao_down = AvailabilityOption.objects.create(id="4", available=False, note="service is down", appname="example2_app")
        ao_down.save()

        a = Availability.objects.create(enabled=ao_down, appname="example2_app")
        a.save()

    def test_get_availability(self):
        client = Client()
        response = client.get(reverse('vosi:availability'))
        self.assertEqual(response.status_code, 200)
        content = response.content
        # remove comment from content
        content = re.sub(r'<!--.*\n.*\n.*\n.*-->\n', '', content)
        #content = content.strip()
        expected = \
u"""<?xml version="1.0" encoding="utf-8"?>
<vosi:availability version="1.1" xmlns:vosi="http://www.ivoa.net/xml/VOSIAvailability/v1.0"><vosi:available>true</vosi:available><vosi:note>Service is ready for requests</vosi:note></vosi:availability>"""
        self.maxDiff = None
        self.assertEqual(content, expected)
