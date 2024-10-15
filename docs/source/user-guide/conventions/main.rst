.. _user-guide_conventions_main:

**************
Basic notation
**************

Vectors
=======

Vectors are represented as a columns of numbers. In Wulfric vectors are stored and
manipulated as (3,) |NumPy|_ arrays:

.. math::

    \boldsymbol{v}
    =
    (v_x,v_y,v_z)^T
    =
    \begin{pmatrix} v_x \\ v_y \\ v_z \end{pmatrix}

.. code-block:: python

    vector = np.array([vx, vy, vz])

.. note::
    One-dimensional |NumPy|_ arrays do not distinguish between row and column vectors.


Cell
====

Cell of the lattice is defined by the three lattice vectors
:math:`\boldsymbol{a}_i = (a_i^x, a_i^y, a_i^z)^T`. In Wulfric those vectors are stored as
a matrix with vectors as rows (hence the transposition symbol):

.. math::

    (\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)^T
    =
    \begin{pmatrix}
      a_1^x & a_1^y & a_1^z \\
      a_2^x & a_2^y & a_2^z \\
      a_3^x & a_3^y & a_3^z
    \end{pmatrix}

.. code-block:: python

    cell = [
        [a1_x, a1_y, a1_z],
        [a2_x, a2_y, a2_z],
        [a3_x, a3_y, a3_z],
    ]

.. note::
    That definition of the cell is the same as in the |spglib-python|_ and is a
    transpose of the definition of the C |spglib|_.

Atom's positions
================

Atoms positions are store as vectors of the relative coordinates with respect to the
cell vectors.

.. math::

    \boldsymbol{r}
    =
    (r_1,r_2,r_3)^T
    =
    \begin{pmatrix} r_1 \\ r_2 \\ r_3 \end{pmatrix}

.. code-block:: python

    position = np.array([r1, r2, r3])

Cartesian (absolute) coordinates of the atoms can be calculated by the following formula:

.. math::

    \boldsymbol{x}^T
    &=
    \boldsymbol{r}^T(\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)^T\\
    \boldsymbol{x}
    &=
    (\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3) \boldsymbol{r}

.. code-block:: python

    x = r @ cell
    # or
    x = cell.T @ r

.. note::

    Remember, that one-dimensional |NumPy|_ arrays do not distinguish between row and
    column vectors and ``cell`` store transposed cell matrix in our notation:
    ``cell`` :math:`\rightarrow (\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)^T`.
    In the documentation analytical formulas are written for the
    :math:`(\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)` matrix, while code
    snippets are written for
    :math:`(\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)^T` matrix.

Reciprocal cell
===============

Reciprocal cell is defined by the three reciprocal lattice vectors
:math:`\boldsymbol{b}_i = (b_i^x, b_i^y, b_i^z)^T`. In Wulfric those vectors are stored as
a matrix with vectors as rows (hence the transposition symbol):

.. math::

    (\boldsymbol{b}_1, \boldsymbol{b}_2, \boldsymbol{b}_3)^T
    =
    \begin{pmatrix}
      b_1^x & b_1^y & b_1^z \\
      b_2^x & b_2^y & b_2^z \\
      b_3^x & b_3^y & b_3^z
    \end{pmatrix}

.. code-block:: python

        reciprocal_cell = [
            [b1_x, b1_y, b1_z],
            [b2_x, b2_y, b2_z],
            [b3_x, b3_y, b3_z],
        ]

Reciprocal cell is connected with the cell of the lattice as follows:

.. math::

    (\boldsymbol{b}_1, \boldsymbol{b}_2, \boldsymbol{b}_3)^T
    =
    2\pi(\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)^{-1}

.. code-block:: python

    reciprocal_cell = 2 * np.pi * np.linalg.inv(cell.T)

K-points
========

K-points are stored as vectors of the fractional coordinates with respect to the
reciprocal cell vectors.

.. math::

    \boldsymbol{g}
    =
    (g_1,g_2,g_3)^T
    =
    \begin{pmatrix} g_1 \\ g_2 \\ g_3 \end{pmatrix}

.. code-block:: python

        kpoint = np.array([g1, g2, g3])

Cartesian (absolute) coordinates of the k-points can be calculated by the following formula:

.. math::

    \boldsymbol{k}^T
    &=
    \boldsymbol{g}^T(\boldsymbol{b}_1, \boldsymbol{b}_2, \boldsymbol{b}_3)^T\\
    \boldsymbol{k}
    &=
    (\boldsymbol{b}_1, \boldsymbol{b}_2, \boldsymbol{b}_3) \boldsymbol{g}

.. code-block:: python

    k = g @ reciprocal_cell
    # or
    k = reciprocal_cell.T @ g




Transformation of the cell
==========================

The choice of the cell of the lattice is not unique. Transformation between two
different cells of the same lattice might be expressed by the transformation matrix
:math:`\boldsymbol{P}`:

.. math::

    (\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)
    =
    (\boldsymbol{\tilde{a}}_1, \boldsymbol{\tilde{a}}_2, \boldsymbol{\tilde{a}}_3) \boldsymbol{P}

.. code-block:: python

    tcell = np.linalg.inv(P.T) @ cell

Crystal is not affected by the change of the cell, i.e. the atom's Cartesian
coordinates are not changed (:math:`\boldsymbol{x} = \boldsymbol{\tilde{x}}`). Therefore,
the atom's relative positions are transformed as

.. math::

    \boldsymbol{\tilde{r}}
    =
    \boldsymbol{P}\boldsymbol{r}

.. code-block:: python

        tr = P @ r

.. hint::

    .. math::

        \boldsymbol{x}
        =
        (\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)\boldsymbol{r}
        =
        (\boldsymbol{\tilde{a}}_1, \boldsymbol{\tilde{a}}_2, \boldsymbol{\tilde{a}}_3)\boldsymbol{P}\boldsymbol{r}
        =
        \boldsymbol{\tilde{x}}
        =
        (\boldsymbol{\tilde{a}}_1, \boldsymbol{\tilde{a}}_2, \boldsymbol{\tilde{a}}_3)\boldsymbol{\tilde{r}}

Reciprocal cell is changed by the transformation as follows:

.. math::

    (\boldsymbol{b}_1, \boldsymbol{b}_2, \boldsymbol{b}_3)
    =
    (\boldsymbol{\tilde{b}}_1, \boldsymbol{\tilde{b}}_2, \boldsymbol{\tilde{b}}_3) (\boldsymbol{P}^{-1})^T

.. code-block:: python

    reciprocal_tcell = np.linalg.inv(P) @ reciprocal_cell

Relative positions of the k-points are transformed as follows:

.. math::

    \boldsymbol{\tilde{g}}
    =
    (\boldsymbol{P}^{-1})^T\boldsymbol{g}

.. code-block:: python

    tg = np.linalg.inv(P).T @ g


.. _user-guide_conventions_main_standardization:

Standardization of the cell
===========================

When standardization of the cell is required, it can be expressed by the
transformation matrix :math:`\boldsymbol{S}` with
:math:`(\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)`
being the standardized primitive cell:

.. math::

    (\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)
    =
    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s) \boldsymbol{S}

.. note::
    Matrix :math:`\boldsymbol{S}` is orthonormal for all Bravais lattices, except for
    the :ref:`guide_mclc`. All matrices satisfy :math:`\det(\boldsymbol{S}) = 1`.


Details on how the standardization matrix is constructed are provided in the individual
pages for each of the 14 :ref:`library_bravais-lattices`.

Conventional vs primitive cell (Setyawan and Curtarolo)
=======================================================

In the reference paper [1]_ conventional (>=1 lattice point per cell) and primitive
(1 lattice point per cell) cells are defined. Transformation from primitive to
conventional cell is expressed by the transformation matrix :math:`\boldsymbol{C}`:

.. math::

    (\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)
    =
    (\boldsymbol{a}_1^c, \boldsymbol{a}_2^c, \boldsymbol{a}_3^c) \boldsymbol{C}

Transformation matrices :math:`\boldsymbol{C}` and its inverse are provided in the individual
pages for each of the 14 :ref:`library_bravais-lattices`.

.. important::
    Given cell is always interpreted as primitive.

References
==========
.. [1] Setyawan, W. and Curtarolo, S., 2010.
    High-throughput electronic band structure calculations: Challenges and tools.
    Computational materials science, 49(2), pp.299-312.
