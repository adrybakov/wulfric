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

  get_N_matrix
  get_niggli


.. _api_cell_kpoints:

K points data
=============

.. autosummary::
  :toctree: generated/

  get_hs_data

.. _api_cell_bravais-lattice:

Bravais lattice constructors as per SC [1]_
===========================================

.. autosummary::
  :toctree: generated/

  get_example_cell_SC
  CUB_SC
  FCC_SC
  BCC_SC
  TET_SC
  BCT_SC
  ORC_SC
  ORCF_SC
  ORCI_SC
  ORCC_SC
  HEX_SC
  RHL_SC
  MCL_SC
  MCLC_SC
  TRI_SC

References
==========
.. [1] Setyawan, W. and Curtarolo, S., 2010.
    High-throughput electronic band structure calculations: Challenges and tools.
    Computational materials science, 49(2), pp. 299-312.
