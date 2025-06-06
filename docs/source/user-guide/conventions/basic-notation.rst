.. _user-guide_conventions_basic-notation:

**************
Basic notation
**************

On this page we introduce formal definition of the vector and cell and describe how they
are stored in wulfric.

Wulfric stores and manipulates both column vectors and row vectors as (3,) |NumPy|_
arrays (i.e. the code does not explicitly distinguish the row and column vectors)

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
Therefore, if the code example contains a vector ``r``, it may mean either
:math:`\boldsymbol{r}` or :math:`\boldsymbol{r}^T`.


Cell
====

Cell of the lattice is defined by the three lattice vectors
:math:`\boldsymbol{a}_i = (a_i^x, a_i^y, a_i^z)^T`. Wulfric stores those vectors as a
matrix of the form

.. math::

    \boldsymbol{A} = (\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)^T
    =
    \begin{pmatrix}
      a_1^x & a_1^y & a_1^z \\
      a_2^x & a_2^y & a_2^z \\
      a_3^x & a_3^y & a_3^z
    \end{pmatrix}

.. code-block:: python

    import numpy as np
    cell = np.array([
        [a1_x, a1_y, a1_z],
        [a2_x, a2_y, a2_z],
        [a3_x, a3_y, a3_z],
    ])

Note that cell is defined as a transpose of the standard definition in |InTabCrys|_ or of
|spglib|_ (However, it is the same as in |spglib-python|_). We deliberatly choose to
define the cell in that way for consistency between the math and python code. Formally
one can substitute :math:`\boldsymbol{A} \rightarrow \boldsymbol{A}^T` and recover the
same formulas as in |InTabCrys|_. We try to define all transformation and rotation
matrices in the same way as in |InTabCrys|_.

Positions of atoms
==================

Atom's positions are stored as vectors of coordinates, that are **relative** with respect
to the cell vectors

.. math::

    \boldsymbol{x}
    =
    (x_1,x_2,x_3)^T
    =
    \begin{pmatrix} x_1 \\ x_2 \\ x_3 \end{pmatrix}

.. code-block:: python

    import numpy as np
    x = np.array([x1, x2, x3])

Cartesian (absolute) coordinates of the atoms (also called "radius vector") can be
calculated as

.. math::

    \boldsymbol{r}^T
    &=
    \boldsymbol{x}^T \boldsymbol{A}\\
    &\text{or}\\
    \boldsymbol{r}
    &=
    \boldsymbol{A}^T \boldsymbol{x}

.. code-block:: python

    r = x @ cell
    # or
    r = cell.T @ x

.. note::

    Remember that one-dimensional |NumPy|_ arrays effectively do not distinguish between
    row and column vectors in the context of matrix multiplication.

Reciprocal cell
===============

Reciprocal cell is defined by three reciprocal lattice vectors
:math:`\boldsymbol{b}_i = (b_i^x, b_i^y, b_i^z)^T`. Wulfric stores those vectors as a
matrix

.. math::

    \boldsymbol{B} = (\boldsymbol{b}_1, \boldsymbol{b}_2, \boldsymbol{b}_3)^T
    =
    \begin{pmatrix}
      b_1^x & b_1^y & b_1^z \\
      b_2^x & b_2^y & b_2^z \\
      b_3^x & b_3^y & b_3^z
    \end{pmatrix}

.. code-block:: python

    import numpy as np
    reciprocal_cell = np.array([
        [b1_x, b1_y, b1_z],
        [b2_x, b2_y, b2_z],
        [b3_x, b3_y, b3_z],
    ])

Reciprocal cell is connected with the direct cell of the lattice as

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
vectors of the reciprocal cell

.. math::

    \boldsymbol{g}
    =
    (g_1,g_2,g_3)^T
    =
    \begin{pmatrix} g_1 \\ g_2 \\ g_3 \end{pmatrix}

.. code-block:: python

    import numpy as np
    g = np.array([g1, g2, g3])

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



.. _user-guide_conventions_basic-notation_transformation:

Transformation of the cell
==========================

For the given lattice the choice of the cell is not unique. Transformation *from* the
original cell :math:`\boldsymbol{A}` *to* the transformed cell
:math:`\boldsymbol{\tilde{A}}` is expressed with the transformation matrix
:math:`\boldsymbol{P}` as

.. math::

    \boldsymbol{\tilde{A}}
    =
    \boldsymbol{P}^T \boldsymbol{A}

.. code-block:: python

    import numpy as np
    # t_cell <- \tilde{A}
    t_cell = P.T @ cell
    cell = np.linalg.inv(P.T) @ t_cell

Note, that we deliberatly define transformation with the transposition sign. Defined in
that way matrix :math:`\boldsymbol{P}` is the same as the transformation matrix
:math:`\boldsymbol{P}` in |InTabCrys|_ Volume A, Chapter 5.1.

It is important to understand that the transformation of the cell describes the *choice*
of the cell for the given *lattice* or *crystal*. In other words while the **cell is
changed**, the **lattice or crystal remain intact**. Consecutively, the **Cartesian
coordinates of atoms are not changed** (:math:`\boldsymbol{r} = \boldsymbol{\tilde{r}}`),
while its **relative coordinates are transformed** as

.. math::

    \boldsymbol{\tilde{x}}
    =
    \boldsymbol{P}^{-1}\boldsymbol{x}

.. code-block:: python

    import numpy as np
    t_x = np.linalg.inv(P) @ x

Reciprocal cell is changed by the transformation as

.. math::

    \boldsymbol{\tilde{B}}
    =
    \boldsymbol{P}^{-1} \boldsymbol{B}

.. code-block:: python

    import numpy as np
    # t_reciprocal_cell <- \tilde{B}
    t_reciprocal_cell = np.linalg.inv(P) @ reciprocal_cell
    reciprocal_cell = P @ t_reciprocal_cell

Relative positions of the k-points are transformed as

.. math::

    \boldsymbol{\tilde{g}}
    =
    \boldsymbol{P}^T\boldsymbol{g}

.. code-block:: python

    import numpy as np
    tg = P.T @ g
