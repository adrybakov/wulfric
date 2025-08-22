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

Cell reduction
==============

.. autosummary::
  :toctree: generated/

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
  SC_CUB
  SC_FCC
  SC_BCC
  SC_TET
  SC_BCT
  SC_ORC
  SC_ORCF
  SC_ORCI
  SC_ORCC
  SC_HEX
  SC_RHL
  SC_MCL
  SC_MCLC
  SC_TRI

Sort later
==========

.. autosummary::
  :toctree: generated/

  get_lattice_points
  get_wigner_seitz_cell
  get_brillouin_zone

References
==========
.. [1] Setyawan, W. and Curtarolo, S., 2010.
    High-throughput electronic band structure calculations: Challenges and tools.
    Computational materials science, 49(2), pp. 299-312.
