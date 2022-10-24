Welcome to Django Contexter's documentation!
==============================================

.. warning::

   This project is under active development

Get data from Django's backend with REST API

Since not all frontend frameworks can use Django context directly, you can create an API. Or use an off-the-shelf API

Installation
------------

To use Django Contexter, first install it using pip:

.. code-block:: console

   pip install django-contexter

Then, you need to add django rest framework to your ``INSTALLED_APPS``:

.. code-block:: Python

    INSTALLED_APPS = [
        ...
        'rest_framework',
        ...
    ]

Contents
--------

.. toctree::

   models

   migration_guides
