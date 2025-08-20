.. _api_crystal:

***************
wulfric.crystal
***************

.. currentmodule:: wulfric.crystal

Basic manipulations
===================

.. autosummary::
    :toctree: generated/

    get_vector
    get_distance
    ensure_000
    shift_atoms
    cure_negative
    get_spatial_mapping

Atoms
=====

.. autosummary::
    :toctree: generated/

    get_atom_species
    populate_atom_species
    ensure_unique_names
    get_spglib_types

Validation of the data
======================

.. autosummary::
    :toctree: generated/

    validate_atoms
    validate_spglib_data

Choice of the cell (or standardization)
=======================================

.. autosummary::
    :toctree: generated/

    get_conventional
    get_primitive
