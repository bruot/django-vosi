===================
Django vosi package
===================

**Implementation of IVOA Support Interfaces as resuable Django app**

This package implements the IVOA Support Interfaces (http://www.ivoa.net/documents/VOSI/20170524/REC-VOSI-1.1.html).
It was intially created for being used with the django-prov_vo package, but can be used with any other package/webapp implementing a Data Access Layer (DAL) interface for the virtual observatory (VO).

**NOTE: This package does not (yet) include all VOSI features.
Created using the specification VOSI 1.1.**


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

* You can add the vosi URLconf to your project's urls.py like this::

    url(r'^vosi/', include('vosi.urls')),

  but usually, you will want to create custom VOSI classes and interfaces inside the corresponding app providing the DAL interface, and thus create url's in their namespace (because the capabilities resource must be a sibling to the DAL resource, see Section 2 of DALI specification).

* Install the requirements of this application, e.g. in a virtual environment::

    virtualenv -p /usr/bin/python2.7 env
    source env/bin/activate

    cd django-prov_vo
    pip install -r requirements.txt

* Run :code:`python manage.py migrate` to update the database and create the provenance models.

TODO
----
* Improve renderer (use lxml?)
* Include more features
* Do proper db tests for availability endpoint