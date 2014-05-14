django-traces
=============

A reusable app to track view hits.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    $ pip install django-traces

To get the latest commit from GitHub

.. code-block:: bash

    $ pip install -e git+git://github.com/bitmazk/django-traces.git#egg=traces

Add ``traces`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'traces',
    )

Add the ``traces`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^traces/', include('traces.urls')),
    )

Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate traces


Usage
-----

If you want to track a certain view just add our middleware::

    MIDDLEWARE_CLASSES = (
        ...
        'traces.middleware.TracesMiddleware',
    )

...and add the view name/url name to the setting TRACED_VIEWS. If you have
added a view like this::

    url(r'^$', TemplateView.as_view(template_name='test.html'), name='test_view'),

...your setting should look like::

    TRACED_VIEWS = ['test_view', ]

The app will now track all visits to this view.


Template tags
-------------

get_view_hits
+++++++++++++

To get the current amount of requests for this view::

    {% load traces_tags %}
    {% get_view_hits as hits %}
    Hits: {{ hits }}

You can also provide the view name to get any view hits::

    {% load traces_tags %}
    {% get_view_hits 'view_name' as hits %}
    Hits: {{ hits }}

    {% get_view_hits 'model_view_name' object as model_view_hits %}
    Hits: {{ model_view_hits }}


Settings
--------

TRACED_VIEWS
++++++++++++

Default: []

List all view names to track.


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-traces
    $ python setup.py install
    $ pip install -r dev_requirements.txt

    $ git co -b feature_branch master
    # Implement your feature and tests
    $ git add . && git commit
    $ git push -u origin feature_branch
    # Send us a pull request for your feature branch
