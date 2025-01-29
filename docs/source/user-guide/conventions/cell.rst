.. _user-guide_conventions_cell:

***********
Which cell?
***********

Some confusion arrives with the term "cell" (unit? primitive? standardized? conventional?).
In this page we explain how Wulfric understand the term "cell" and it's variants.

Summary of the cell is presented in the picture below. For the details on how
transformation matrices :math:`\boldsymbol{C}` and :math:`\boldsymbol{S}` act see
:ref:`user-guide_conventions_main_transformation`.

.. figure:: ../../img/cell-relations.png
    :align: center
    :target: ../../_images/cell-relations.png

"The" cell
===========

The basic ``cell`` of the package. In the context of the lattice it is understood as
primitive. In context of the crystal (i.e. ``cell`` and ``atoms``) it is *interpreted* by
the package as primitive cell, however, it might not be the actual primitive cell of the
crystal structure.


.. _user-guide_conventions_cell_standardization:

Standardized cells
==================

Standardization of Wulfric follows the Setyawan and Curtarolo [1]_ paper (SC paper),
although in the future we might implement other standardization conventions (open a
:ref:`contribute_feature` if you are interested). In the SC paper two types of the cell
are defined: conventional one and primitive one. We use transformation matrix
:math:`\boldsymbol{S}` to compute the **standardized primitive** cell

.. math::

    \boldsymbol{A}
    =
    \boldsymbol{S}^T \boldsymbol{A^S}

and transformation matrix :math:`\boldsymbol{C}` to compute the **standardized
conventional** cell

.. math::


    \boldsymbol{A^s}
    =
    \boldsymbol{C}^T \boldsymbol{A^{cs}}

Details on the construction of matrices :math:`\boldsymbol{S}` and exact forms of matrices
:math:`\boldsymbol{C}` are provided in the individual pages for each of the 14
:ref:`user-guide_conventions_bravais-lattices`.

Matrix :math:`\boldsymbol{S}` is orthonormal for all Bravais lattices, except for
the :ref:`guide_mclc`. All matrices satisfy :math:`\det(\boldsymbol{S}) = 1`.

Primitive cell contains exactly 1 lattice point per cell, while conventional cell might
include more than one lattice point.

Note, that in the individual pages for Bravais lattices standardized cells are written
in the default orientation as in the SC paper. However, Wulfric deals with
arbitrary orientation of the the cell (consequently, the crystal) and automatically
recomputes relative coordinates of the high symmetry k-points with respect to the
orientation of the crystall (i.e. given ``cell``). Standardization
(:py:func:`.cell.get_standardized`) might change the choice of the cell, but will not
change the orientation of the crystal in the real space. Standardization
(:py:func:`.crystal.standardize`) might change relative coordinates of atoms, but will
not change their position in the real space.

References
==========
.. [1] Setyawan, W. and Curtarolo, S., 2010.
    High-throughput electronic band structure calculations: Challenges and tools.
    Computational materials science, 49(2), pp.299-312.
