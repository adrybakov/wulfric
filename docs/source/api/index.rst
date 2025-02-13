.. module:: wulfric

.. _api:

*************
API reference
*************

:Release: |version|

The main interface to the package should be imported as

.. doctest::

   >>> import wulfric as wulf
   >>> # or
   >>> import wulfric

Sub-modules
===========
.. toctree::
    :maxdepth: 1

    cell
    constants
    crystal
    io
    visualization
    geometry

Classes
=======

.. autosummary::
    :toctree: generated/

    Kpoints

Top-level functions
===================


.. autosummary::
    :toctree: generated/

    compare_numerically
    print_2d_array
    logo

Exceptions
==========


.. autosummary::
    :toctree: generated/

    StandardizationTypeMismatch
    FailedToDeduceAtomSpecies
    NiggliReductionFailed
