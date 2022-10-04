Model's API
===========

Instalation
+++++++++++

1. Add ``django_contexter.models`` to your ``INSTALLED_APPS``:

.. code-block:: Python

   INSTALLED_APPS = [
      'rest_framework',
      ...
      'django_contexter.models',
      ...
   ]

2. Add path in your root ``urls.py``:

.. code-block:: Python

    urlpatterns = [
      ...
      path('api/models/', include("django_contexter.models.urls")),
      ...
   ]

Configuration
+++++++++++++

``CONTEXTER_ACCESS_POLICY`` is a pretty powerful way to set up access and here's how to use it:

.. warning::

    ``__all__``, ``__remaining__`` and ``__undeclared__`` are special key words and are used as **strings**\ , not **lists**

Global models access
--------------------

This is an example of the simplest policy:

.. code-block:: Python

    CONTEXTER_ACCESS_POLICY = {
        "allow_methods": "__all__", # 1
        "allow_models": "__all__", # 2
        "reject_models": [] # 3
    }

1. Allow **all** methods(about methods later)

2. Allow **all** models

3. Don't forbid **any** model(about the difference between *allow* and *reject* later)

Although it's simple, it's not safe at all. What if someone wants to see the ``auth.User`` model?:

.. code-block:: Python

    CONTEXTER_ACCESS_POLICY = {
        "allow_methods": "__all__", # 1
        "allow_models": "__all__", # 2
        "reject_models": ["auth.User"] # 3
    }

Now we still allow everything,
but because of the difference between ``reject`` and ``allow``,
you can now access **all** models **except** ``auth.User``

.. note::

    It is important to note that this works because ``reject`` is considered a higher priority than ``allow``

But to declare each prohibited model is very long and difficult - yes, so we can ban all models that are not allowed:

.. code-block:: Python

    CONTEXTER_ACCESS_POLICY = {
        "allow_methods": "__all__", # 1
        "allow_models": ["auth.Permission"], # 2
        "reject_models": "__remaining__" # 3
    }

This literally bans all models **except** those in ``allowed_models``

Now we can get access **only** to the ``auth.Permission``

But usually you have more than one model, so you have a choice: keywords **or** a list of models

Here's how you can:

1. Allow **only** ``auth.Permission`` *and* ``auth.User``

.. code-block:: Python

    CONTEXTER_ACCESS_POLICY = {
        "allow_methods": "__all__", # 1
        "allow_models": ["auth.Permission", "auth.User"], # 2
        "reject_models": "__remaining__" # 3
    }

2. Prohibit **only** auth.Permission *and* auth.User

.. note::

    This works just like ``__remaining__`` from ``reject_models`` (it works **only** because ``reject_models`` are higher priority)

.. code-block:: Python

    CONTEXTER_ACCESS_POLICY = {
        "allow_methods": "__all__", # 1
        "allow_models": "__all__", # 2
        "reject_models": ["auth.Permission", "auth.User"] # 3
    }

3. Prohibit **only** ``auth.User`` *and* allow **only** ``auth.Permission``

.. code-block:: Python

    CONTEXTER_ACCESS_POLICY = {
        "allow_methods": "__all__", # 1
        "allow_models": ["auth.User"], # 2
        "reject_models": ["auth.Permission"] # 3
    }

Global methods access
---------------------

.. note::

    In allow_methods, the **only** ``__all__`` keyword works

It's certainly all very interesting.
But what if we want to forbid certain methods,
because there are so many of them in the `QuerySet API <https://docs.djangoproject.com/en/4.1/ref/models/querysets/#queryset-api>`_?:

.. code-block:: Python

    CONTEXTER_ACCESS_POLICY = {
        "allow_methods": ["all", "get"], # 1
        "allow_models": ["auth.User"],
        "reject_models": ["auth.Permission"] # 2
    }

With this access policy you can:

1. Gain access **only** to the ``.get(**model_request)`` and ``.all()``
2. ...And **only** to ``auth.Permission``

Individual settings for models
------------------------------

So far, we have been thinking globally.
What if we need to allow ``.get(**model_request)`` and ``.all()`` methods for ``auth.User``, but only ``.get(**model_request)`` for ``auth.Permission``?:

.. code-block:: Python

    CONTEXTER_ACCESS_POLICY = {
        "allow_methods": "__all__", # 1
        "allow_models": "__all__", # 2
        "reject_models": "__undeclared__", # 3

        "auth.User": { # recorded extended
            "allow_methods": ["all", "get"], # 4
            "hidden_fields": [] # We will consider this later
        },

        "auth.Permission": { # recorded extended
            "allow_methods": ["get"], # 5
            "hidden_fields": [] # We will consider this later
        }
    }

.. note::

    __undeclared__ means all models that are recorded extended

1. **Globally** allow all methods
2. **Globally** allow all models
3. **Globally** forbid all models that aren't recorded extended
4. **Locally** allow ``.get(**model_request)`` and ``.all()`` methods
5. **Locally** allow only ``.get(**model_request)`` method

What is the difference between global and local? - local is a higher priority and overrides global

Hide fields
-----------

.. warning::

    ``hidden_fields`` is a mandatory parameter, it must always be present

.. code-block:: Python

    CONTEXTER_ACCESS_POLICY = {
        "allow_methods": "__all__",
        "allow_models": "__all__",
        "reject_models": "__undeclared__",

        "auth.User": { # recorded extended
            "allow_methods": ["all", "get"],
            "hidden_fields": [] # 1
        },

        "auth.Permission": { # recorded extended
            "allow_methods": ["get"],
            "hidden_fields": [] # 2
        }
    }

1 and 2 are local field hiding points

Let's try to hide ``codename`` from ``auth.Permission``:

.. code-block:: Python

    CONTEXTER_ACCESS_POLICY = {
        "allow_methods": "__all__",
        "allow_models": "__all__",
        "reject_models": "__undeclared__",

        "auth.User": { # recorded extended
            "allow_methods": ["all", "get"],
            "hidden_fields": [] # 1
        },

        "auth.Permission": { # recorded extended
            "allow_methods": ["get"],
            "hidden_fields": ["codename"] # 2
        }
    }

Here's the server response (we'll look at the API later):

.. code-block:: JSON

    {
        "id": 1,
        "name": "Can add log entry",
        "codename": "********",
        "content_type": 1
    }

This works for several fields as well:

.. code-block:: Python

    CONTEXTER_ACCESS_POLICY = {
        "allow_methods": "__all__",
        "allow_models": "__all__",
        "reject_models": "__undeclared__",

        "auth.User": { # recorded extended
            "allow_methods": ["all", "get"],
            "hidden_fields": [] # 1
        },

        "auth.Permission": { # recorded extended
            "allow_methods": ["get"],
            "hidden_fields": ["codename", "name"] # 2
        }
    }

Here's the server response:

.. code-block:: JSON

    {
        "id": 1,
        "name": "****",
        "codename": "********",
        "content_type": 1
    }

Hiding fields using a custom function
-------------------------------------

We're reaching a new level of customizability:

.. note::

    You need to pass a **reference** to the function:

    Not your_func\ **()**\ , your_func <-- without ``()``

.. code-block:: Python

    def custom_hide(full_result, model, props, field, request):
        print(full_result)
        print(model)
        print(props)
        print(field)
        print(request)

        return "CUSTOM_HIDED"

    CONTEXTER_ACCESS_POLICY = {
        "allow_methods": "__all__",
        "allow_models": "__all__",
        "reject_models": "__undeclared__",

        "auth.User": { # recorded extended
            "allow_methods": ["all", "get"],
            "hidden_fields": []
        },

        "auth.Permission": { # recorded extended
            "allow_methods": ["get"],
            "hidden_fields": [], # 1
            "codename": custom_hide # 2
        }
    }

Console output:

``admin | log entry | Can add log entry`` - full result

``<class 'django.contrib.auth.models.Permission'>`` - model object

``{'allow_methods': ['get'], 'hidden_fields': [], 'codename': <function custom_hide at 0x7fe305d2b0a0>}`` - your config

``auth.Permission.codename`` - field object

``<rest_framework.request.Request: GET '/api/models/?modelName=auth.Permission&get=%7B%22pk%22:%201%7D'>`` - request object

The server response:

.. code-block:: JSON

    {
        "id": 1,
        "name": "Can add log entry",
        "codename": "CUSTOM_HIDED",
        "content_type": 1
    }

.. note::

    You cannot change the names of the arguments

As you can see, your method is called with the parameters ``full_result``, ``model``, ``props``, ``field``, ``request``

And you can return any **text** - it will replace the field value

QuerySet API method lists
-------------------------

First of all, perform the import:

.. code-block:: Python

    from django_contexter.models.method_types import *

Lists:

.. option:: METHODS_THAT_RENTURN_NEW_QUERYSET

   :description: Django provides a range of QuerySet refinement methods that modify either the types of results returned by the QuerySet or the way its SQL query is executed

   :link: `#methods-that-return-new-querysets <https://docs.djangoproject.com/en/4.1/ref/models/querysets/#methods-that-return-new-querysets>`_

.. option:: METHODS_THAT_DO_NOT_RETURN_QUERYSET

   :description: The following QuerySet methods evaluate the QuerySet and return something other than a QuerySet

   :link: `#methods-that-do-not-return-querysets <https://docs.djangoproject.com/en/4.1/ref/models/querysets/#methods-that-do-not-return-querysets>`_

.. option:: METHODS_THAT_CHAGES_RECORDS

   :description: Methods for changing the database

.. option:: ASYNC_METHODS_THAT_DO_NOT_RETURN_QUERYSET

   :description: Same as ``METHODS_THAT_DO_NOT_RETURN_QUERYSET`` - asynchronous method variations

.. option:: ASYNC_METHODS_THAT_CHAGES_RECORDS

   :description: Same as ``METHODS_THAT_CHAGES_RECORDS`` - asynchronous method variations

.. option:: UNSAFE_METHODS

   :description: Alias for ``METHODS_THAT_CHAGES_RECORDS``

.. option:: ASYNC_UNSAFE_METHODS

   :description: Alias for ``ASYNC_METHODS_THAT_CHAGES_RECORDS``

.. option:: ALL_UNSAFE_METHODS

   :description: ``ASYNC_METHODS_THAT_CHAGES_RECORDS`` and ``METHODS_THAT_CHAGES_RECORDS``

.. option:: ALL_METHODS

   :description: All QuerySet API methods

.. option:: ALL_SAFE_METHODS

   :description: ``ALL_METHODS`` without ``ALL_UNSAFE_METHODS``

API Documentation
+++++++++++++++++

.. note::

   Requests is chainable

.. note::

    | ``/api/models/`` - you set this in your urls.py
    |
    | This is omitted here, for example:
    | ``/api/models/?modelName=auth.Permission`` --> ``?modelName=auth.Permission``

.. note::

    Technically, this library supports all QuerySet API methods. But you still can't apply any changes to the database

Parmeter\(s\)
-------------

.. option:: modelName

   :required: Yes

   :many: No

   :description: Defines the model for the following commands

   :example: ?modelName=Permission ...

   :parameter type: String

How do you build requests?
--------------------------

1. Same as in Django:

.. code-block:: Python

    <MODEL_NAME>.objects.all().get(pk=1)

API Equivalent:

.. code-block::

    ?modelName=<MODEL_NAME>&all=&get={"pk": 1}

2. Or an example with filter\ **s**\ :

.. note::

    | Actually the digit after the **keyword** has no meaning and is used for uniqueness in the query (address string)
    |
    | For example: in the query below there are keywords: all and filter

.. code-block:: Python

    <MODEL_NAME>.objects.all() \
                        .filter(name__contains="can") \
                        .filter(name__contains="get")

API Equivalent:

.. code-block::

    ?modelName=<MODEL_NAME>&all&filter1={"name__contains": "can"}&filter2={"name__contains": "get"}

And so you can build any query using QuerySet API methods

Errors
------

-----------
Error codes
-----------

.. option:: 0 or NO_MANDATORY_PARAMETER_MODELNAME

   :description: There is no ``modelName`` parameter in the query

.. option:: 1 or MODEL_DOES_NOT_EXIST

   :description: No model corresponding to ``modelName``

.. option:: 2 or FUNCTION_DOES_NOT_EXIST_IN_QUERYSET_API

   :description: The called method does not exist

.. option:: 3 or FIELD_ERROR

   :description: The field in use does not exist

.. option:: 4 or REJECT_ERROR

   :description: Request rejected according to the Access Policy

.. option:: 5 or SERVER_WRONG_CONFIG

   :description: Error in configuration

-----------------------
Errors in configuration
-----------------------

1. ``allow_models`` and ``reject_models`` are both ``__all__``
2. The same model is in ``allow_models`` and ``reject_models`` at the same time
3. Using ``allow_models`` as ``__all__`` and ``reject_models`` as ``__remaining__`` at the same time
