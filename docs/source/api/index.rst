.. module:: wulfric

.. _api:

*************
API reference
*************

:Release: |version|

The main interface to the package should be imported as

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

    compare_numerically
    add_sugar
    remove_sugar
    logo
    get_spglib_types
    get_spglib_data
    validate_spglib_data

Exceptions
==========
.. autosummary::
    :caption: Exceptions
    :toctree: generated/

    StandardizationTypeMismatch
    FailedToDeduceAtomSpecies
    NiggliReductionFailed

Legacy code
===========
.. autosummary::
    :caption: Legacy code
    :toctree: generated/

    lepage
