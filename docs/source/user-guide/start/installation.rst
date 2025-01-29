.. _user-guide_start_installation:

************
Installation
************

Requirement for wulfric installation are:

* |Python|_ (>=3.9)
* |NumPy|_ (~=1.26)
* |SciPy|_
* |termcolor|_
* |matplotlib|_ (optional: [visual])
* |plotly|_ (optional: [visual])

Most likely Python is already installed on your machine (if not check these links:
|Python-installation|_).

Wulfric can be installed with :ref:`pip <installation-pip>` or from
:ref:`source <installation-source>`.

Check Python
============

The easiest way to check if you have python installed
is to run the following command in your terminal::

  python

If you see something like::

  Python 3.10.9 (main, Dec 15 2022, 18:25:35) [Clang 14.0.0 (clang-1400.0.29.202)] on darwin
  Type "help", "copyright", "credits" or "license" for more information.
  >>>

then you have python installed.

In most cases ``python`` command launches python3, however if it launches python2, then
you may need to use ``python3`` instead (and ``pip3`` instead of ``pip`` in the following
commands).

.. hint::
  Use ``exit()`` or press ``ctrl+D`` to close python console.

.. _installation-pip:

Installation with pip
=====================

To install wulfric, run (you may need to use ``pip3``)::

  pip install wulfric

Optionally, if you want to use :ref:`visualization <user-guide_module_plotting>`
capabilities of wulfric, you can install |matplotlib|_ and/or |plotly|_
by yourself or install them with wulfric::

  pip install wulfric[visual]

.. note::
  You may need to escape the ``[`` and ``]`` characters from your shell, because they are
  special characters in most shells. For example, in bash you can use backslash to escape
  them::

    pip install wulfric\[visual\]

  Or enclose full name in quotes::

    pip install "wulfric[visual]"

.. _installation-source:

Installation from source
========================

* Clone the project to your local computer::

    git clone git@github.com:adrybakov/wulfric.git

* Change the directory::

    cd wulfric

* Install the requirements::

    pip install -r requirements.txt

.. note:: If you check the content of the ``requirements.txt`` file:

  .. literalinclude:: ../../../../requirements.txt

  You'll see that all dependencies - mandatory and optional - are installed. If you prefer
  to install only mandatory dependencies, you can do it manually.

* To install wulfric, run (you may need to use ``pip3``)::

    pip install wulfric

Update
======

If you want to update the package to the latest available version (|version|)
type the following in your terminal (you may need to use ``pip3``)::

  pip install wulfric --upgrade
