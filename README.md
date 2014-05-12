django-traces
=============

A reusable app to track view hits

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    $ pip install django-traces

To get the latest commit from GitHub

.. code-block:: bash

    $ pip install -e git+git://github.com/bitmazk/django-traces.git#egg=traces

TODO: Describe further installation steps (edit / remove the examples below):

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

TODO


Settings
--------

FIRST SETTING
+++++++++++++

Default: None

TODO


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
