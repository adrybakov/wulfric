.. _api_cell:

************
wulfric.cell
************

.. currentmodule:: wulfric.cell


Basic manipulations
===================

.. autosummary::
  :toctree: generated/

  get_params
  from_params
  get_reciprocal
  get_scalar_products
  is_reasonable

Cell reduction
==============

.. autosummary::
  :toctree: generated/

  niggli


Bravais lattice type
====================

.. autosummary::
  :toctree: generated/

  lepage
  get_variation
  get_name
  get_centring_type
  get_crystal_family
  get_pearson_symbol

.. _api_cell_bravais-lattice:

Bravais lattice constructors
============================

.. autosummary::
  :toctree: generated/

  get_cell_example
  CUB
  FCC
  BCC
  TET
  BCT
  ORC
  ORCF
  ORCI
  ORCC
  HEX
  RHL
  MCL
  MCLC
  TRI

Standardization (SC)
====================

.. autosummary::
  :toctree: generated/

  get_standardized
  get_S_matrix

Convetional cell (SC)
=====================

.. autosummary::
  :toctree: generated/

  get_conventional
  get_C_matrix


Other
=====

.. autosummary::
  :toctree: generated/

  get_voronoi_cell
