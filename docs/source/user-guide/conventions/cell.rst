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

.. note::
    We use :py:class:`.Lattice` in the examples, but the same logic applies to it's
    children classes (e.g. :py:class:`.Crystal`).

"The" cell
===========

The main cell in the package resides in the :py:attr:`.Lattice.cell` attribute.
In context of the :py:class:`.Lattice` class it is undestood to be primitive cell, as it
defines the lattice. In context of the :py:class:`.Crystal` class (i.e.
:py:attr:`.Crystal.cell`) it is *interpreted* by the package as primitive cell, however,
it might not be the actual primitive cell of the crystal structure.

Every other type of the cell (including reciprocal cell
:py:attr:`.Lattice.reciprocal_cell`) is defined by some transformation of
:py:attr:`.Lattice.cell`.


.. _user-guide_conventions_cell_standardization:

Standardized cells
==================

Standardization of Wulfric follows the Setyawan and Curtarolo [1]_ paper (SC paper),
although in the future we might implement other standardization conventions (open a
:ref:`contribute_feature` if you are interested). In the SC paper two types of the cell
are defined: conventional one and primitive one. We use transformation matrix
:math:`\boldsymbol{S}` to compute the **standardized primitive** cell

.. math::

    (\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)
    =
    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s) \boldsymbol{S}

and transformation matrix :math:`\boldsymbol{C}` to compute the **standardized
conventional** cell

.. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (\boldsymbol{a}_1^{cs}, \boldsymbol{a}_2^{cs}, \boldsymbol{a}_3^{cs}) \boldsymbol{C}.

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
