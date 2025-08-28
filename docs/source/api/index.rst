.. module:: wulfric

.. _api:

*************
API reference
*************

:Release: |version|

Wulfric is usually imported as

.. doctest::

    >>> import wulfric


.. toctree::
    :caption: Submodules
    :maxdepth: 1

    cell
    crystal
    kpoints
    constants/index
    io
    geometry


Classes
=======

.. autosummary::
    :caption: Classes
    :toctree: generated/

    Kpoints
    PlotlyEngine
    SyntacticSugar


Top level functions
===================

.. autosummary::
    :caption: Top level functions
    :toctree: generated/

    compare_with_tolerance
    add_sugar
    remove_sugar
    logo


Spglib interface
================

.. autosummary::
    :caption: Top level functions
    :toctree: generated/

    get_spglib_types
    get_spglib_data
    validate_spglib_data


Exceptions
==========

.. autosummary::
    :caption: Exceptions
    :toctree: generated/

    ConventionNotSupported
    FailedToDeduceAtomSpecies
    NiggliReductionFailed
    PotentialBugError


Legacy code
===========

.. note::
    Legacy code is not used by wulfric internally. It is completely separated from the
    package. It will not be supported nor updated. In the future it may be removed.

.. autosummary::
    :caption: Legacy code
    :toctree: generated/

    lepage
