.. module:: wulfric

.. _api:

*************
API reference
*************

:Release: |version|

The main interface to the package should be imported as

.. doctest::

   >>> import wulfric
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
    geometry

Classes
=======

.. autosummary::
    :toctree: generated/

    Kpoints
    PlotlyEngine

Top-level functions
===================


.. autosummary::
    :toctree: generated/

    compare_numerically
    add_sugar
    remove_sugar
    logo

Exceptions
==========


.. autosummary::
    :toctree: generated/

    StandardizationTypeMismatch
    FailedToDeduceAtomSpecies
    NiggliReductionFailed


Legacy code
===========


.. autosummary::
  :toctree: generated/

  lepage
