.. module:: wulfric

.. _api:

*************
API reference
*************

:Release: |version|

The reference manual describes modules and their objects,
which may be used for the postprocessing.
The main interface to the package may be imported as

.. code-block:: python

   import wulfric as wulf

In the examples across the documentation it is expected to be imported in that way.



Sub-modules
===========
.. toctree::
    :maxdepth: 1

    cell
    constants
    crystal
    interfaces
    io
    visualization
    geometry

Top-level functions
===================


.. autosummary::
    :toctree: generated/

    compare_numerically
    print_2d_array
    logo
    copyright
    warranty

Exceptions
==========


.. autosummary::
    :toctree: generated/

    StandardizationTypeMismatch
    FailedToDeduceAtomSpecies
