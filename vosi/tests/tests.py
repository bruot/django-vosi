# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client
from django.test.utils import setup_test_environment

from vosi.models import Availability, AvailabilityOption
from vosi.models import VOResource_Capability, VOResource_Interface, VOResource_AccessURL
from vosi.renderers import VosiAvailabilityRenderer, VosiCapabilityRenderer


def remove_comment(content):
    content = re.sub(r'<!--.*\n.*\n.*\n.*-->\n', '', content)
    return content

class VosiAvailabilityRenderer_TestCase(TestCase):

    def test_availability_render(self):
        data = {'available': 'true', 'note': 'Service is available'}
        response = VosiAvailabilityRenderer().render(data)
        response = remove_comment(response)
        expected = \
u"""<?xml version="1.0" encoding="utf-8"?>
<vosi:availability version="1.1" xmlns:vosi="http://www.ivoa.net/xml/VOSIAvailability/v1.0"><vosi:available>true</vosi:available><vosi:note>Service is available</vosi:note></vosi:availability>"""
        self.maxDiff = None
        self.assertEqual(response, expected)

    def test_availability_render_pretty(self):
        data = {'available': 'true', 'note': 'Service is available'}
        response = VosiAvailabilityRenderer().render(data, prettyprint=True)
        expected = \
u"""<vosi:availability xmlns:vosi="http://www.ivoa.net/xml/VOSIAvailability/v1.0" version="1.1">
  <vosi:available>true</vosi:available>
  <vosi:note>Service is available</vosi:note>
</vosi:availability>
"""
        self.assertEqual(response, expected)


class VosiCapabilityRenderer_TestCase(TestCase):

    def setUp(self):
        cap = VOResource_Capability.objects.create(
            id="1",
            standardID='ivo://ivoa.net/std/ExampleDM#DAL',
            description='Example model',
            appname="example1")
        cap.save()

        iface = VOResource_Interface.objects.create(
            id="2",
            type="vs:ParamHTTP",
            capability=cap,
            version="1.0",
            role='std'
        )
        iface.save()

        aurl = VOResource_AccessURL.objects.create(
            interface=iface,
            url="http://www.example.com/mydalinterface/",
            use="full"
        )
        aurl.save()
        data = VOResource_Capability.objects.all()

    def test_capabilities_render(self):
        data = VOResource_Capability.objects.filter(appname='example1').order_by('id')
        response = VosiCapabilityRenderer().render(data)
        response = remove_comment(response)
        expected = \
u"""<?xml version="1.0" encoding="utf-8"?>
<vosi:capabilities xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1" xmlns:vs="http://www.ivoa.net/xml/VODataService/v1.1" xmlns:vosi="http://www.ivoa.net/xml/VOSICapabilities/v1.0"><capability standardID="ivo://ivoa.net/std/ExampleDM#DAL"><interface xsi:type="vs:ParamHTTP"><accessURL use="full">http://www.example.com/mydalinterface/</accessURL></interface></capability></vosi:capabilities>"""
        self.maxDiff = None
        self.assertEqual(response, expected)

    def test_capabilities_render_pretty(self):
        data = VOResource_Capability.objects.filter(appname='example1').order_by('id')
        response = VosiCapabilityRenderer().render(data, prettyprint=True)
        response = remove_comment(response)
        expected = \
"""<vosi:capabilities xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:vs="http://www.ivoa.net/xml/VODataService/v1.1" xmlns:vosi="http://www.ivoa.net/xml/VOSICapabilities/v1.0" version="1.1">
  <capability standardID="ivo://ivoa.net/std/ExampleDM#DAL">
    <interface xsi:type="vs:ParamHTTP">
      <accessURL use="full">http://www.example.com/mydalinterface/</accessURL>
    </interface>
  </capability>
</vosi:capabilities>
"""
        self.maxDiff = None
        self.assertEqual(response, expected)


class Vosi_TestCase(TestCase):
    def setUp(self):
        ao_up = AvailabilityOption.objects.create(id="1", available=True, note="service is up", appname="example1")
        ao_up.save()

        ao_down = AvailabilityOption.objects.create(id="2", available=False, note="service is down", appname="example1")
        ao_down.save()

        a = Availability.objects.create(enabled=ao_up, appname="example1")
        a.save()

        ao_up = AvailabilityOption.objects.create(id="3", available=True, note="This service is up", appname="example2")
        ao_up.save()

        ao_down = AvailabilityOption.objects.create(id="4", available=False, note="This service is down", appname="example2")
        ao_down.save()

        a = Availability.objects.create(enabled=ao_down, appname="example2")
        a.save()

        cap = VOResource_Capability.objects.create(
            id="1",
            standardID='ivo://ivoa.net/std/ExampleDM#DAL',
            description='Example model',
            appname="example1")
        cap.save()

        iface = VOResource_Interface.objects.create(
            id="2",
            type="vs:ParamHTTP",
            capability=cap,
            version="1.0",
            role='std'
        )
        iface.save()

        aurl = VOResource_AccessURL.objects.create(
            interface=iface,
            url="http://www.example.com/mydalinterface/",
            use="full"
        )
        aurl.save()

        cap = VOResource_Capability.objects.create(
            id="2",
            standardID='ivo://ivoa.net/std/Example2DM#DAL',
            description='Example2 model',
            appname="example2")
        cap.save()

        iface = VOResource_Interface.objects.create(
            id="3",
            type="vs:ParamHTTP",
            capability=cap,
            version="2.0",
            role='std'
        )
        iface.save()

        aurl = VOResource_AccessURL.objects.create(
            interface=iface,
            url="http://www.example2.com/mydalinterface/",
            use="full"
        )
        aurl.save()


    def test_get_availability(self):
        client = Client()
        response = client.get(reverse('vosi:availability'))
        self.assertEqual(response.status_code, 200)
        content = response.content
        # remove comment from content
        content = re.sub(r'<!--.*\n.*\n.*\n.*-->\n', '', content)

        expected = \
u"""<?xml version="1.0" encoding="utf-8"?>
<vosi:availability version="1.1" xmlns:vosi="http://www.ivoa.net/xml/VOSIAvailability/v1.0"><vosi:available>true</vosi:available><vosi:note>Service is ready for requests</vosi:note></vosi:availability>"""
        self.maxDiff = None
        self.assertEqual(content, expected)

    def test_get_availability_example1(self):
        client = Client()
        #how to set: request.resolver_match.app_name = 'example_app'??
        response = client.get(reverse('example1:availability'))#, app_name = 'example_app'))
        self.assertEqual(response.status_code, 200)
        content = response.content
        # remove comment from content
        content = re.sub(r'<!--.*\n.*\n.*\n.*-->\n', '', content)

        expected = \
u"""<?xml version="1.0" encoding="utf-8"?>
<vosi:availability version="1.1" xmlns:vosi="http://www.ivoa.net/xml/VOSIAvailability/v1.0"><vosi:available>true</vosi:available><vosi:note>service is up</vosi:note></vosi:availability>"""
        self.maxDiff = None
        self.assertEqual(content, expected)

    def test_get_availability_example2(self):
        client = Client()
        #how to set: request.resolver_match.app_name = 'example_app'??
        response = client.get(reverse('example2:availability'))#, app_name = 'example_app'))
        self.assertEqual(response.status_code, 200)
        content = response.content
        # remove comment from content
        content = re.sub(r'<!--.*\n.*\n.*\n.*-->\n', '', content)

        expected = \
u"""<?xml version="1.0" encoding="utf-8"?>
<vosi:availability version="1.1" xmlns:vosi="http://www.ivoa.net/xml/VOSIAvailability/v1.0"><vosi:available>false</vosi:available><vosi:note>This service is down</vosi:note></vosi:availability>"""
        self.maxDiff = None
        self.assertEqual(content, expected)


    def test_get_capabilities(self):
        client = Client()
        response = client.get(reverse('vosi:capabilities'))
        self.assertEqual(response.status_code, 200)
        content = response.content
        # remove comment from content
        content = re.sub(r'<!--.*\n.*\n.*\n.*-->\n', '', content)
        expected = \
u"""<?xml version="1.0" encoding="utf-8"?>
<vosi:capabilities xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1" xmlns:vs="http://www.ivoa.net/xml/VODataService/v1.1" xmlns:vosi="http://www.ivoa.net/xml/VOSICapabilities/v1.0"><capability standardID="ivo://ivoa.net/std/ExampleDM#DAL"><interface xsi:type="vs:ParamHTTP"><accessURL use="full">http://www.example.com/mydalinterface/</accessURL></interface></capability><capability standardID="ivo://ivoa.net/std/Example2DM#DAL"><interface xsi:type="vs:ParamHTTP"><accessURL use="full">http://www.example2.com/mydalinterface/</accessURL></interface></capability></vosi:capabilities>"""
        self.maxDiff = None
        self.assertEqual(content, expected)

    def test_get_capabilities_example1(self):
        client = Client()
        response = client.get(reverse('example1:capabilities'))
        self.assertEqual(response.status_code, 200)
        content = response.content
        # remove comment from content
        content = re.sub(r'<!--.*\n.*\n.*\n.*-->\n', '', content)
        expected = \
u"""<?xml version="1.0" encoding="utf-8"?>
<vosi:capabilities xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1" xmlns:vs="http://www.ivoa.net/xml/VODataService/v1.1" xmlns:vosi="http://www.ivoa.net/xml/VOSICapabilities/v1.0"><capability standardID="ivo://ivoa.net/std/ExampleDM#DAL"><interface xsi:type="vs:ParamHTTP"><accessURL use="full">http://www.example.com/mydalinterface/</accessURL></interface></capability></vosi:capabilities>"""
        self.maxDiff = None
        self.assertEqual(content, expected)

    def test_get_capabilities_example2(self):
        client = Client()
        response = client.get(reverse('example2:capabilities'))
        self.assertEqual(response.status_code, 200)
        content = response.content
        # remove comment from content
        content = re.sub(r'<!--.*\n.*\n.*\n.*-->\n', '', content)
        expected = \
u"""<?xml version="1.0" encoding="utf-8"?>
<vosi:capabilities xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1" xmlns:vs="http://www.ivoa.net/xml/VODataService/v1.1" xmlns:vosi="http://www.ivoa.net/xml/VOSICapabilities/v1.0"><capability standardID="ivo://ivoa.net/std/Example2DM#DAL"><interface xsi:type="vs:ParamHTTP"><accessURL use="full">http://www.example2.com/mydalinterface/</accessURL></interface></capability></vosi:capabilities>"""
        self.maxDiff = None
        self.assertEqual(content, expected)
