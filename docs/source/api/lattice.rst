.. _api_lattice:

*******
Lattice
*******

.. currentmodule:: wulfric

Class
=====

.. autosummary::
    :toctree: generated/

    Lattice

Cell standardization
====================

.. autosummary::
    :toctree: generated/

    Lattice.standardize



Lattice parameters
==================

Real space (primitive cell)
---------------------------

.. autosummary::
    :toctree: generated/

    Lattice.cell
    Lattice.a1
    Lattice.a2
    Lattice.a3
    Lattice.a
    Lattice.b
    Lattice.c
    Lattice.alpha
    Lattice.beta
    Lattice.gamma
    Lattice.unit_cell_volume
    Lattice.parameters

Real space (conventional cell)
------------------------------

.. autosummary::
    :toctree: generated/

    Lattice.conv_cell
    Lattice.conv_a1
    Lattice.conv_a2
    Lattice.conv_a3
    Lattice.conv_a
    Lattice.conv_b
    Lattice.conv_c
    Lattice.conv_alpha
    Lattice.conv_beta
    Lattice.conv_gamma
    Lattice.conv_unit_cell_volume
    Lattice.conv_parameters

Reciprocal space
----------------

.. autosummary::
    :toctree: generated/

    Lattice.reciprocal_cell
    Lattice.rcell
    Lattice.b1
    Lattice.b2
    Lattice.b3
    Lattice.k_a
    Lattice.k_b
    Lattice.k_c
    Lattice.k_alpha
    Lattice.k_beta
    Lattice.k_gamma
    Lattice.reciprocal_cell_volume
    Lattice.reciprocal_parameters
    Lattice.kpoints

Information properties
======================

.. autosummary::
    :toctree: generated/

    Lattice.type
    Lattice.variation
    Lattice.name
    Lattice.pearson_symbol
    Lattice.centring_type
    Lattice.crystal_family

Numerical accuracy
==================

.. autosummary::
    :toctree: generated/

    Lattice.eps
    Lattice.eps_rel
    Lattice.angle_tol

Independent copy
================

.. autosummary::
    :toctree: generated/

    Lattice.copy
