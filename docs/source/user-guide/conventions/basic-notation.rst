.. _user-guide_conventions_basic-notation:

**************
Basic notation
**************

On this page we introduce formal definition of the vector and cell and describe how they
are stored in wulfric.

Wulfric stores and manipulates both column vectors and row vectors as (3,) |NumPy|_
arrays (i. e. the code does not explicitly distinguish the row and column vectors)

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

.. _user-guide_conventions_basic-notation_cell:

Cell
====

Cell is defined by three lattice vectors (or "basis vectors")
:math:`\boldsymbol{a}_i = (a_i^x, a_i^y, a_i^z)^T`. Wulfric stores those vectors in a form
of as a :math:`(3\times3)` matrix

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

where each vector is a row


.. code-block:: python

    a1 = cell[0]
    a2 = cell[1]
    a3 = cell[2]

.. note::

    Wulfric defines cell as a transpose of the standard definition in |InTabCrys|_ or of
    |spglib|_ (However, it is the same as in |spglib-python|_).

    We deliberately choose to define the cell in that way for consistency between the
    mathematical formulas and python code. Formally one can substitute
    :math:`\boldsymbol{A} = \boldsymbol{A}^T_{\text{ITA}}` and recover the same formulas
    as in |InTabCrys|_ for most cases. We try to define the action of the transformation
    and rotation matrices in the same way as in |InTabCrys|_.

.. _user-guide_conventions_basic-notation_position-of-atom:

Position of atom
================

Atom's position can be stored in two distinct ways

*   :math:`\boldsymbol{r}` - as absolute position in the global Cartesian reference
    frame
*   :math:`\boldsymbol{x}` - as relative position with respect to some
    :ref:`user-guide_conventions_basic-notation_cell`

In wulfric atom's position is **always** stored and returned as **relative**.

.. math::

    \boldsymbol{x}
    =
    (x_1,x_2,x_3)^T
    =
    \begin{pmatrix} x_1 \\ x_2 \\ x_3 \end{pmatrix}

.. code-block:: python

    import numpy as np
    x = np.array([x1, x2, x3])

Cartesian (absolute) position of the atom (also called "radius vector") can be
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

.. _user-guide_conventions_basic-notation_reciprocal-cell:

Reciprocal cell
===============

Reciprocal cell is defined by three reciprocal lattice vectors
:math:`\boldsymbol{b}_i = (b_i^x, b_i^y, b_i^z)^T`.  Wulfric stores those vectors in a
form of as a :math:`(3\times3)` matrix

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

.. _user-guide_conventions_basic-notation_k-points:

K-points
========

Similar to :ref:`user-guide_conventions_basic-notation_position-of-atom`, k-point can
be stored in two distinct ways

*   :math:`\boldsymbol{k}` - as absolute position in the global Cartesian reference
    frame

    .. math::

        \boldsymbol{k}
        =
        (k_1,k_2,k_3)^T
        =
        \begin{pmatrix} k_1 \\ k_2 \\ k_3 \end{pmatrix}

    .. code-block:: python

        import numpy as np
        k = np.array([k1, k2, k3])

*   :math:`\boldsymbol{g}` - as relative position with respect to some
    :ref:`user-guide_conventions_basic-notation_reciprocal-cell`

    .. math::

        \boldsymbol{g}
        =
        (g_1,g_2,g_3)^T
        =
        \begin{pmatrix} g_1 \\ g_2 \\ g_3 \end{pmatrix}

    .. code-block:: python

        import numpy as np
        g = np.array([g1, g2, g3])

In wulfric k-point's storage/return mode can be controlled with the keyword argument
``relative=True`` or ``relative=False`` in almost all functions and methods. Often
``relative=True`` by default.

With the known cell :math:`\boldsymbol{B}` change between relative and absolute k point
position is straightforward

*   Relative -> absolute

    .. math::

        \boldsymbol{k}^T
        &=
        \boldsymbol{g}^T
        \boldsymbol{B}\\
        \boldsymbol{k}
        &=
        \boldsymbol{B}^T \boldsymbol{g}

    .. code-block:: python

        k = g @ reciprocal_cell
        # or
        k = reciprocal_cell.T @ g

*   Cartesian (absolute) ->  relative

    .. math::

        \boldsymbol{g}^T
        &=
        \boldsymbol{k}^T
        \boldsymbol{B}^{-1}\\
        \boldsymbol{g}
        &=
        \left(\boldsymbol{B}^T\right)^{-1} \boldsymbol{k}

    .. code-block:: python

        g = k @ np.linalg.inv(reciprocal_cell)
        # or
        g = np.linalg.inv(reciprocal_cell.T) @ k



.. _user-guide_conventions_basic-notation_transformation:

Transformation of the cell
==========================

Choice of the cell is not unique for any given lattice. Transformation *from* the
original cell :math:`\boldsymbol{A}` *to* the transformed cell
:math:`\boldsymbol{\tilde{A}}` is expressed with the transformation matrix
:math:`\boldsymbol{P}` as

.. math::

    \boldsymbol{\tilde{A}}
    =
    \boldsymbol{P}^T
    \boldsymbol{A}

.. code-block:: python

    import numpy as np
    # tilde_cell is \tilde{A}
    tilde_cell = P.T @ cell
    cell = np.linalg.inv(P.T) @ tilde_cell


.. note::
    We deliberately define action of the  transformation with the transposition sign.
    When its action is defined in that way matrix :math:`\boldsymbol{P}` is the same as
    the transformation matrix :math:`\boldsymbol{P}` in |InTabCrys|_ Volume A, Chapter 5.1.

It is important to understand that the transformation of the cell describes the *choice*
of the cell for the given *lattice* or *crystal*. In other words while the **cell is
changed**, the **lattice or crystal remains intact**. Consecutively, the **Cartesian**
position of atom is **not changed** (:math:`\boldsymbol{r} = \boldsymbol{\tilde{r}}`),
while its **relative** position is **transformed** as

.. math::

    \boldsymbol{\tilde{x}}
    &=
    \boldsymbol{P}^{-1}
    \boldsymbol{x} \\
    \boldsymbol{\tilde{x}}^T
    &=
    \boldsymbol{x}^T
    (\boldsymbol{P}^{-1})^T

.. code-block:: python

    import numpy as np
    tilde_x = np.linalg.inv(P) @ x
    # or
    tilde_x = x @ np.linalg.inv(P).T

Reciprocal cell is changed by the transformation as

.. math::

    \boldsymbol{\tilde{B}}
    =
    \boldsymbol{P}^{-1} \boldsymbol{B}

.. code-block:: python

    import numpy as np
    # tilde_reciprocal_cell <- \tilde{B}
    tilde_reciprocal_cell = np.linalg.inv(P) @ reciprocal_cell
    reciprocal_cell = P @ tilde_reciprocal_cell

**Cartesian** position of k-point does **not change**, but **relative** position of
k-point is **transformed** as

.. math::

    \boldsymbol{\tilde{g}}
    &=
    \boldsymbol{P}^T
    \boldsymbol{g}\\
    \boldsymbol{\tilde{g}}^T
    &=
    \boldsymbol{g}^T
    \boldsymbol{P}

.. code-block:: python

    import numpy as np
    tilde_g = P.T @ g
    # or
    tilde_g = g @ P

Transformation matrix itself can be computed from original and transformed direct cells
(implemented in :py:func:`wulfric.cell.get_transformation_matrix`)

.. math::

    \boldsymbol{P}
    =
    (\boldsymbol{A}^{-1})^T
    \boldsymbol{\tilde{A}}^T

.. code-block:: python

    import numpy as np
    P = np.linalg.inv(cell).T @ tilde_cell

or from original and transformed reciprocal cells

.. math::

    \boldsymbol{P}
    =
    \boldsymbol{B}
    \boldsymbol{\tilde{B}}^{-1}

.. code-block:: python

    import numpy as np
    tilde_reciprocal_cell = np.linalg.inv(P) @ reciprocal_cell
    reciprocal_cell = P @ tilde_reciprocal_cell

.. _user-guide_conventions_basic-notation_rotation:

Rotation of the cell
====================

On contrary to the :ref:`user-guide_conventions_basic-notation_transformation`, rotation
changes the orientation of  the lattice or crystal, while keeping the same choice of the
cell.

Rotation of the given cell :math:`\boldsymbol{A}` *from* its original orientation *to* the
new orientation of the same cell :math:`\boldsymbol{A}_{\text{rotated}}` is expressed with
the rotation matrix :math:`\boldsymbol{R}` as

.. math::

    \boldsymbol{A}_{\text{rotated}}
    =
    \boldsymbol{A}
    \boldsymbol{R}^T

.. code-block:: python

    import numpy as np
    # rotated_cell is A_{rotated}
    rotated_cell =  cell @ R.T
    # Note that inverse of rotation matrix is equivalent to its transpose
    cell = rotated_cell @ R

If action of the rotation matrix is defined as above, then it acts on the column vectors
in the usual way

.. math::

    \boldsymbol{v}_{\text{rotated}}
    &=
    \boldsymbol{R}
    \boldsymbol{v}\\
    \boldsymbol{v}_{\text{rotated}}^T
    &=
    \boldsymbol{v}^T
    \boldsymbol{R}^T

.. code-block:: python

    v_rotated = R @ v
    # or
    v_rotated = v @ R.T

.. note::

    Remember that one-dimensional |NumPy|_ arrays effectively do not distinguish between
    row and column vectors in the context of matrix multiplication.

**Relative** position of atom is **not changed** by the rotation
(:math:`\boldsymbol{x} = \boldsymbol{\tilde{x}}`), while its **Cartesian** position is
**rotated** as


.. math::

    \boldsymbol{r}_{\text{rotated}}
    &=
    \boldsymbol{R}
    \boldsymbol{r}\\
    \boldsymbol{r}_{\text{rotated}}^T
    &=
    \boldsymbol{r}^T
    \boldsymbol{R}^T

.. code-block:: python

    import numpy as np
    r_rotated = R @ r
    # or
    r_rotated = r @ R.T

Reciprocal cell is rotated as

.. math::

    \boldsymbol{B}_{\text{rotated}}
    =
    \boldsymbol{B}
    \boldsymbol{R}^T

.. code-block:: python

    import numpy as np
    # reciprocal_cell_rotated is B_{rotated}
    reciprocal_cell_rotated = reciprocal_cell @ R.T
    # Note that inverse of rotation matrix is equivalent to its transpose
    reciprocal_cell = reciprocal_cell_rotated @ R

**Relative** position of the k-point do **not change**, but **Cartesian** position of
k-point is **rotated** as

.. math::

    \boldsymbol{k}_{\text{rotated}}
    &=
    \boldsymbol{R}
    \boldsymbol{k}\\
    \boldsymbol{k}_{\text{rotated}}^T
    &=
    \boldsymbol{k}^T
    \boldsymbol{R}^T

.. code-block:: python

    import numpy as np
    k_rotated = R @ k
    # or
    k_rotated = k @ R.T

Rotation matrix itself can be computed from original and rotated direct cells


.. math::

    \boldsymbol{R}
    =
    \boldsymbol{A}_{\text{rotated}}^{-1}
    \boldsymbol{A}

.. code-block:: python

    import numpy as np
    R = np.linalg.inv(cell_rotated) @ cell

or from original and transformed reciprocal cells

.. math::

    \boldsymbol{R}
    =
    \boldsymbol{B}_{\text{rotated}}^{-1}
    \boldsymbol{B}

.. code-block:: python

    import numpy as np
    R = np.linalg.inv(reciprocal_cell_rotated) @ reciprocal_cell
