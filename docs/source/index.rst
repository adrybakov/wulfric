.. toctree::
    :maxdepth: 1
    :hidden:

    user-guide/installation
    User Guide <user-guide/index>
    api/index
    release-notes/index
    contribute/index
    cite
    support

:Release: |version|
:Date: |release_date|

**Useful links**:
:ref:`Installation <user-guide_start_installation>` |
`Issue Tracker <https://github.com/adrybakov/wulfric/issues>`_ |
:ref:`Cite us <wulfric_cite>` |
:ref:`user-support`

****************
What is wulfric?
****************

Wulfric is a python package for the crystal structures. It uses concepts of
``cell``, ``atoms``, ``k-points`` and provides a simple skeleton for the user to built on
(see :ref:`user-guide_usage_key-concepts`).

The functionality of wulfric includes (but not limited to):

*   Choice of the conventional and primitive cells
    (:ref:`user-guide_conventions_which-cell`).

*   Automatic choice of the :ref:`Kpoints <user-guide_usage_kpoints>`
    and k-path for all :ref:`Bravais lattice types <user-guide_conventions_bravais-lattices>`
    and space groups.

*   Full support for Setyawan and Curtarolo ("SC") convention. See
    :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc` for examples.
*   Full support for Hinuma, Pizzi, Kumagai, Oba, Tanaka ("HPKOT") convention. Wulfric
    follows the paper, but provides an implementation alternative to |seekpath|_. See
    :ref:`sphx_glr_user-guide_conventions_bravais-lattices_1_hpkot` for examples.
*   Convenient interface to part of |spglib|_. All symmetry-related functions of wulfric
    are powered by |spglib|_. To read more see :ref:`user-guide_usage_spglib-interface`.

*   Visualization of cells, atoms, lattices and crystals. See
    :ref:`user-guide_usage_visualization` for examples.

*   Common :ref:`user-guide_usage_cell` and :ref:`user-guide_usage_crystal`.

*************************************
How is this documentation structured?
*************************************

*   Code examples are given in the :ref:`user-guide`.
*   Full public API is described in :ref:`api`.
*   To get some support and ask questions see :ref:`user-support`.
*   To understand how wulfric performs transformations and rotations, how it stores cells,
    atom positions and k-points see :ref:`user-guide_conventions_basic-notation` and
    :ref:`user-guide_usage_key-concepts`.
*   To understand the difference between various cells see
    :ref:`user-guide_conventions_which-cell`.
*   To see examples of what wulfric can visualize see
    :ref:`user-guide_usage_visualization_examples`.
