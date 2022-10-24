Migration Guides
================

These version guides, which offer backward-uncompatible changes, will help you upgrade to the new version

V1.0.0
++++++

Changes
-------

In this version, there have been changes to the Access Policy,
and more specifically to ``hidden_fields``.
Instead of using a list with hidden fields and individual elements to functionally hide:

Before:

.. code-block:: Python

    CONTEXTER_ACCESS_POLICY = {
        "allow_methods": ALL_METHODS,
        "allow_models": "__remaining__",
        "reject_models": "__undeclared__",

        "auth.Permission": {
            "allow_methods": ["get"],
            "hidden_fields": ["name"],
            "codename": custom_hide
        }
    }

After:

.. code-block:: Python

    CONTEXTER_ACCESS_POLICY = {
        "allow_methods": ALL_METHODS,
        "allow_models": "__remaining__",
        "reject_models": "__undeclared__",

        "auth.Permission": {
            "allow_methods": ["get"],
            "hidden_fields": {
                "codename": custom_hide,
                "name": "****"
            },
        }
    }

How to migrate?:
----------------

--------
Step One
--------

Change the hidden_fields to dictionary(``{}``\ )

Before:

.. code-block:: Python

    #...
    "hidden_fields": []
    #...

After:

.. code-block:: Python

    #...
    "hidden_fields": {}
    #...

--------
Step Two
--------

Write down the fields you've hidden in a simple way (see example below)

Before:

.. code-block:: Python

    #...
    "hidden_fields": ["name"]
    #...

After:

.. note::

    1. You can put anything JSON serializable

.. code-block:: Python

    #...
    "hidden_fields": {
        "name": "****" # 1
    }
    #...

----------
Step Three
----------

Write down the fields you've hidden in a functional way (see example below)

Before:

.. code-block:: Python

    #...
    "hidden_fields": {
        "name": "****"
    },
    "codename": custom_hide
    #...

After:

.. note::

    1. You can put anything JSON serializable

.. code-block:: Python

    #...
    "hidden_fields": {
        "name": "****",
        "codename": custom_hide
    },
    #...

----
Done
----

Congratulations 🥳

You have just successfully migrated to version 1.0.0
