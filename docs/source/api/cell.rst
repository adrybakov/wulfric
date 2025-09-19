.. _api_cell:

************
wulfric.cell
************

.. currentmodule:: wulfric.cell


Lattice and lattice parameters
==============================

.. autosummary::
    :toctree: generated/

    get_params
    from_params
    get_scalar_products
    get_lattice_points


Cell's derivatives
==================

.. autosummary::
    :toctree: generated/

    get_reciprocal
    get_wigner_seitz_cell
    get_brillouin_zone
    get_niggli


Cell'stransformations
=====================

.. autosummary::
    :toctree: generated/

    get_transformation_matrix


.. _api_cell_sc-bravais-lattice-examples:

SC convention [1]_
==================

.. autosummary::
    :toctree: generated/

    sc_get_example
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


References
==========
.. [1] Setyawan, W. and Curtarolo, S., 2010.
    High-throughput electronic band structure calculations: Challenges and tools.
    Computational materials science, 49(2), pp. 299-312.
