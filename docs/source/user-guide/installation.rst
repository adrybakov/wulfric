.. _user-guide_start_installation:

************
Installation
************

Requirement for wulfric installation are:

* |Python|_ (>=3.9)

And several libraries:

.. literalinclude:: ../../../requirements.txt


Wulfric can be installed with :ref:`pip <installation-pip>` or from
:ref:`source <installation-source>`.

.. hint::

    Use

    .. code-block:: bash

        python --version

    to check which version of python is available.

Do you have Python?
===================

Most likely Python is already installed on your machine (if not check these links:
|Python-installation|_).

One of the ways to check if you have python installed is to execute the following command
in your terminal

.. code-block:: bash

    python

If you see something like

.. code-block:: bash

    Python 3.10.9 (main, Dec 15 2022, 18:25:35) [Clang 14.0.0 (clang-1400.0.29.202)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

then you have it.

In most cases ``python`` command launches python3, however if it launches python2, then
you may need to use ``python3`` instead (and ``pip3`` instead of ``pip`` in the following).

.. hint::
    Use ``exit()`` or press ``ctrl+D`` to close python console.

.. _installation-pip:

Installation with pip
=====================

To install wulfric use the command (you may need to use ``pip3``)

.. code-block:: bash

    pip install wulfric

Optionally, if you want to use :ref:`visualization <user-guide_usage_visualization>`
capabilities of wulfric, you can install |plotly|_ and |scipy|_ manually or install them
with wulfric as

.. code-block:: bash

    pip install wulfric[visual]

.. note::
    You may need to escape the ``[`` and ``]`` characters, because they are special
    characters in most shells. For example, in bash you can use backslash to escape them

    .. code-block:: bash

        pip install wulfric\[visual\]

    Or enclose full name in quotes

    .. code-block:: bash

        pip install "wulfric[visual]"

.. hint::
    If you are using |jupyter|_, then wulfric can be installed with

    .. code-block::

        %pip install wulfric

    within it.

.. _installation-source:

Installation from source
========================

*   Clone the project to your local computer

    .. code-block:: bash

        git clone git@github.com:adrybakov/wulfric.git

*   Change the directory

    .. code-block:: bash

        cd wulfric

*   Install the requirements

    .. code-block:: bash

        pip install -r requirements.txt

    You'll see that all dependencies (both mandatory and optional) are installed. If you
    prefer to install only mandatory dependencies, then you can do it manually.

*   To install wulfric, run (you may need to use ``pip3``)

    .. code-block:: bash

        pip install .

Update
======

If you want to update the package to the latest available version (|version|),
then use the command (you may need to use ``pip3``)

.. code-block:: bash

    pip install wulfric --upgrade
