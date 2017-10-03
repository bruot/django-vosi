===================
Django vosi package
===================

**Implementation of IVOA Support Interfaces as resuable Django app**

This package implements the `IVOA Support Interfaces <http://www.ivoa.net/documents/VOSI/20170524/REC-VOSI-1.1.html>`_.
It was intially created for being used with the
`django-prov_vo <https://github.com/kristinriebe/django-prov_vo>`_
package together with a web application like
`provenance-rave <https://github.com/kristinriebe/provenance-rave>`_,
but can be used with any other package/webapp implementing a Data
Access Layer (DAL) interface for the virtual observatory (VO).
Inspired by Daiquiri's VOSI implementation for TAP
(`django-daiquiri <https://github.com/aipescience/django-daiquiri/>`_).

**NOTE: This package does not (yet) include all VOSI features.
Created using the VOSI specification version 1.1.**


Installation
------------

* Download the package::

       git clone https://github.com/github/kristinriebe/django-vosi/

* Package the prov_vo app::

       cd django-vosi
       python setup.py sdist

* Switch to your main web application (or create it now with :code:`django-admin startproject <my_web_app>`)::

    cd ..
    cd <my_web_app>

  An example for a django project using this package is available at https://github.com/kristinriebe/provenance-rave

* Install the vosi app (e.g. inside your virtual environment) using pip::

    pip install ../django-vosi/dist/django-vosi-0.1.tar.gz

  Alternatively, you can also add the following lines in your projects's :code:`settings.py`::

    import sys
    sys.path.append('../django-vosi/')


* Add vosi to your INSTALLED_APPS setting in :code:`settings.py` like this::

    INSTALLED_APPS = [
        ...
        'vosi',
    ]

* You *could* add the vosi URLconf to your project's urls.py like this::

    url(r'^vosi/', include('vosi.urls')),

  But most likely you need to copy the VOSI url's to the :code:`urls.py` file of your main project/package providing the data access layer interface::


    from django.conf.urls import url, include
    import vosi.urls

    urlpatterns = [
      ...
      url(r'^availability/$', vosi.views.availability, name='vosi_availability'),
      url(r'^capabilities/$', vosi.views.capabilities, name='vosi_capabilities'),
    ]

  This is necessary, because the capabilities resource must be a sibling to the DAL resource, see Section 2 of `DALI <http://www.ivoa.net/documents/DALI/20170517/REC-DALI-1.1.html>`_ specification.

* Install the requirements of this application, e.g. in a virtual environment::

    virtualenv -p /usr/bin/python2.7 env
    source env/bin/activate

    cd django-vosi
    pip install -r requirements.txt

* Run :code:`python manage.py migrate` to update the database and create the VOSI database tables.

* Inser the VOSI data specific for your web application, see `django-prov_vo <https://github.com/kristinriebe/django-prov_vo>`_ for an example.


Testing
-----------

* This django application can be tested standalone, outside the project. First create a virtual environment and install the required python (2.7) packages::

    virtualenv -p /usr/bin/python2.7 env
    source env/bin/activate

    pip install -r requirements.txt

* Now switch to vosi and run::

    cd vosi
    python runtests.py

* This runs all the tests stored in :code:`tests`.


TODO
----
* Implement tables endpoint as well
* Improve renderer (use lxml?)
* Include more features (missing attributes for availability)
* Write more tests
* Use admin interface to adjust availability options and set availability
