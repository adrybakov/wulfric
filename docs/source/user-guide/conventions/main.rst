.. _user-guide_conventions_main:

**************
Basic notation
**************

On this page we introduce formal definition of the vector and cell and how they stored in
wulfric.

In wulfric both column vectors and row vectors are stored and manipulated as (3,)
|NumPy|_ arrays (i.e. the code does not explicitly distinguish the row and column vectors):

.. math::

    \boldsymbol{v}_{column}
    &=
    \begin{pmatrix} v_x \\ v_y \\ v_z \end{pmatrix}\\
    \boldsymbol{v}_{row}
    &=
    ( v_x, v_y, v_z )\\


.. code-block:: python

    import numpy as np
    vector_column = np.array([vx, vy, vz])
    vector_row = np.array([vx, vy, vz])

When simply the word "vector" is used, we assume a column vector for the mathematical
formulas.

.. math::

    \boldsymbol{v}
    &=
    \begin{pmatrix} v_x \\ v_y \\ v_z \end{pmatrix}


.. code-block:: python

    import numpy as np
    vector = np.array([vx, vy, vz])

One-dimensional |NumPy|_ arrays do not distinguish between row and column vectors.
Therefore, if the code example use a vector ``r``, it might mean either
:math:`\boldsymbol{r}` or :math:`\boldsymbol{r}^T`.


Cell
====

Cell of the lattice is defined by the three lattice vectors
:math:`\boldsymbol{a}_i = (a_i^x, a_i^y, a_i^z)^T`. In wulfric those vectors are stored as
a matrix of the form:

.. math::

    \boldsymbol{A} = (\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)^T
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

Above definition of the cell is the same as in the |spglib-python|_.

Atom's positions
================

Atoms positions are stored as vectors of the relative coordinates with respect to the
cell vectors.

.. math::

    \boldsymbol{r}
    =
    (r_1,r_2,r_3)^T
    =
    \begin{pmatrix} r_1 \\ r_2 \\ r_3 \end{pmatrix}

.. code-block:: python

    import numpy as np
    position = np.array([r1, r2, r3])

Cartesian (absolute) coordinates of the atoms can be calculated as

.. math::

    \boldsymbol{x}^T
    &=
    \boldsymbol{r}^T \boldsymbol{A}\\
    &\text{or}\\
    \boldsymbol{x}
    &=
    \boldsymbol{A}^T \boldsymbol{r}

.. code-block:: python

    x = r @ cell
    # or
    x = cell.T @ r

.. note::

    Remember, that one-dimensional |NumPy|_ arrays do not distinguish between row and
    column vectors.

Reciprocal cell
===============

Reciprocal cell is defined by the three reciprocal lattice vectors
:math:`\boldsymbol{b}_i = (b_i^x, b_i^y, b_i^z)^T`. In wulfric those vectors are stored as
a matrix

.. math::

    \boldsymbol{B} = (\boldsymbol{b}_1, \boldsymbol{b}_2, \boldsymbol{b}_3)^T
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

    \boldsymbol{B}
    =
    2\pi(\boldsymbol{A}^T)^{-1}

.. code-block:: python

    import numpy as np
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

    import numpy as np
    kpoint = np.array([g1, g2, g3])

Cartesian (absolute) coordinates of the k-points can be calculated as

.. math::

    \boldsymbol{k}^T
    &=
    \boldsymbol{g}^T \boldsymbol{B}\\
    \boldsymbol{k}
    &=
    \boldsymbol{B}^T \boldsymbol{g}

.. code-block:: python

    k = g @ reciprocal_cell
    # or
    k = reciprocal_cell.T @ g



.. _user-guide_conventions_main_transformation:

Transformation of the cell
==========================

The choice of the cell of the lattice is not unique. Transformation of the original cell
:math:`\boldsymbol{A}` to the transformed cell :math:`\boldsymbol{\tilde{A}}` is expressed
with the transformation matrix :math:`\boldsymbol{P}`:

.. math::

    \boldsymbol{A}
    =
    \boldsymbol{P}^T \boldsymbol{\tilde{A}}

.. code-block:: python

    import numpy as np
    cell = P.T @ tcell
    # tcell <- \tilde{A}
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
        \boldsymbol{A}^T \boldsymbol{r}
        =
        \boldsymbol{\tilde{A}}^T \boldsymbol{P} \boldsymbol{r}
        =
        \boldsymbol{\tilde{x}}
        =
        \boldsymbol{\tilde{A}}^T \boldsymbol{\tilde{r}}

Reciprocal cell is changed by the transformation as follows:

.. math::

    \boldsymbol{B}
    =
    \boldsymbol{P}^{-1} \boldsymbol{\tilde{B}}

.. code-block:: python

    import numpy as np
    reciprocal_cell = np.linalg.inv(P) @ reciprocal_tcell
    # reciprocal_tcell <- \tilde{B}
    reciprocal_tcell = P @ reciprocal_cell

Relative positions of the k-points are transformed as follows:

.. math::

    \boldsymbol{\tilde{g}}
    =
    (\boldsymbol{P}^{-1})^T\boldsymbol{g}

.. code-block:: python

    import numpy as np
    tg = np.linalg.inv(P).T @ g
