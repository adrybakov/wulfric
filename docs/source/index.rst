*******
Wulfric
*******

.. toctree::
    :maxdepth: 1
    :hidden:

    user-guide/installation
    User Guide <user-guide/index>
    api/index
    release-notes/index
    contribute/index
    cite
    support

:Release: |version|
:Date: |release_date|

**Useful links**:
:ref:`Installation <user-guide_start_installation>` |
`Issue Tracker <https://github.com/adrybakov/wulfric/issues>`_ |
:ref:`Cite us <wulfric_cite>` |
:ref:`support`

****************
What is wulfric?
****************

Wulfric is a python package for the description and symmetries of crystal structures.
It uses a simple concepts of ``cell`` and ``atoms`` and provides a simple skeleton for
other codes to built on. (see :ref:`user-guide_usage_key-concepts`)

The functional of wulfric includes (but not limited to):

* Calculation of Bravais lattice type and variation.

* Automatic choice of the :ref:`Kpoints <user-guide_usage_kpoints>`
  and K-path for all :ref:`Bravais lattice types <user-guide_conventions_bravais-lattices>`.

* Set of useful functions for :ref:`user-guide_usage_cell`, :ref:`user-guide_usage_crystal`.

* Standalone :py:func:`.lepage` and :py:func:`.niggli` algorithms.

Installation
============

As any other Python package::

  pip install wulfric

For the full guide on wulfric installation see :ref:`user-guide_start_installation`.

How to import wulfric
=====================

To use wulfric in your code import it in a following way:

.. code-block:: python

    import wulfric as wulf

The shorten import name ``wulf`` simplifies the readability of python code.
It is used in the examples and we encourage you to try it.

Further reading
===============

Good starting point is the :ref:`user-guide_usage_key-concepts` page.
Afterwards we recommend to continue with the :ref:`user-guide_fundamentals`,
where examples are given.

For the full technical reference of the public part of the package see :ref:`api`.

Some of the algorithms implemented in wulfric are described in the
:ref:`user-guide_library`.

For the full description of adopted Bravais lattices and high-symmetry K-points
see :ref:`user-guide_conventions_bravais-lattices`.

.. note::
  The images are interactive over there.

.. note::
  The terminal output is colored by default. However, we respect `NO_COLOR <https://no-color.org/>`_.
