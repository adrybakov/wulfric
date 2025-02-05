.. _guide_orc:

******************
Orthorhombic (ORC)
******************

**Pearson symbol**: oP

**Constructor**:  :py:func:`.ORC`

It is defined by three parameters :math:`a`, :math:`b` and :math:`c` with
:math:`a < b < c`. Standardized primitive and conventional cells in the default
orientation are

.. math::

  \begin{matrix}
  \boldsymbol{a}_1^s &=& \boldsymbol{a}_1^{cs} &=& (a, &0, &0)\\
  \boldsymbol{a}_2^s &=& \boldsymbol{a}_2^{cs} &=& (0, &b, &0)\\
  \boldsymbol{a}_3^s &=& \boldsymbol{a}_3^{cs} &=& (0, &0, &c)
  \end{matrix}

Transformation matrix from standardized primitive cell to standardized conventional cell
is

.. include:: C_matrix.inc


K-path
======

:math:`\mathrm{\Gamma-X-S-Y-\Gamma-Z-U-R-T-Z\vert Y-T\vert U-X\vert S-R}`

=======================  ================================  ================================  ================================
Point                    :math:`\times\boldsymbol{b}_1^s`  :math:`\times\boldsymbol{b}_2^s`  :math:`\times\boldsymbol{b}_3^s`
=======================  ================================  ================================  ================================
:math:`\mathrm{\Gamma}`  :math:`0`                         :math:`0`                         :math:`0`
:math:`\mathrm{R}`       :math:`1/2`                       :math:`1/2`                       :math:`1/2`
:math:`\mathrm{S}`       :math:`1/2`                       :math:`1/2`                       :math:`0`
:math:`\mathrm{T}`       :math:`0`                         :math:`1/2`                       :math:`1/2`
:math:`\mathrm{U}`       :math:`1/2`                       :math:`0`                         :math:`1/2`
:math:`\mathrm{X}`       :math:`1/2`                       :math:`0`                         :math:`0`
:math:`\mathrm{Y}`       :math:`0`                         :math:`1/2`                       :math:`0`
:math:`\mathrm{Z}`       :math:`0`                         :math:`0`                         :math:`1/2`
=======================  ================================  ================================  ================================

Variations
==========

There are no variations for orthorhombic lattice.
One example is predefined: ``orc`` with
:math:`a = \pi`, :math:`b  = 1.5\pi` and :math:`c = 2\pi`.

Examples
========

Brillouin zone and default kpath
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: orc_brillouin.py
    :language: py

.. raw:: html
    :file: orc_brillouin.html

Primitive and conventional cell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: orc_real.py
    :language: py

.. raw:: html
    :file: orc_real.html

Wigner-Seitz cell
^^^^^^^^^^^^^^^^^
.. literalinclude:: orc_wigner-seitz.py
    :language: py

.. raw:: html
    :file: orc_wigner-seitz.html

Cell standardization
====================

Lengths of the lattice vectors have to satisfy
:math:`\vert\boldsymbol{a}_1^s\vert < \vert\boldsymbol{a}_2^s\vert < \vert\boldsymbol{a}_3^s\vert`
for the primitive cell in a standard form.


* If :math:`\vert \boldsymbol{a}_3\vert > \vert \boldsymbol{a}_2\vert > \vert \boldsymbol{a}_1\vert`,
  then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)

  and

  .. math::

    \boldsymbol{S}
    =
    \boldsymbol{S}^{-1}
    =
    \boldsymbol{S}^T
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}

* If :math:`\vert \boldsymbol{a}_3\vert > \vert \boldsymbol{a}_1\vert > \vert \boldsymbol{a}_2\vert`,
  then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (-\boldsymbol{a}_2, -\boldsymbol{a}_1, -\boldsymbol{a}_3)

  and

  .. math::

    \boldsymbol{S}
    =
    \boldsymbol{S}^{-1}
    =
    \boldsymbol{S}^T
    =
    \begin{pmatrix}
      0 & -1 & 0 \\
      -1 & 0 & 0 \\
      0 & 0 & -1
    \end{pmatrix}

* If :math:`\vert \boldsymbol{a}_2\vert > \vert \boldsymbol{a}_3\vert > \vert \boldsymbol{a}_1\vert`,
  then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (-\boldsymbol{a}_1, -\boldsymbol{a}_3, -\boldsymbol{a}_2)

  and

  .. math::

    \boldsymbol{S}
    =
    \boldsymbol{S}^{-1}
    =
    \boldsymbol{S}^T
    =
    \begin{pmatrix}
      -1 & 0 & 0 \\
      0 & 0 & -1 \\
      0 & -1 & 0
    \end{pmatrix}

* If :math:`\vert \boldsymbol{a}_2\vert > \vert \boldsymbol{a}_1\vert > \vert \boldsymbol{a}_3\vert`,
  then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (\boldsymbol{a}_3, \boldsymbol{a}_1, \boldsymbol{a}_2)

  and

  .. math::

    \boldsymbol{S} =
    \begin{pmatrix}
      0 & 0 & 1 \\
      1 & 0 & 0 \\
      0 & 1 & 0
    \end{pmatrix}
    \qquad
    \boldsymbol{S}^{-1}
    =
    \boldsymbol{S}^T
    =
    \begin{pmatrix}
      0 & 1 & 0 \\
      0 & 0 & 1 \\
      1 & 0 & 0
    \end{pmatrix}

* If :math:`\vert \boldsymbol{a}_1\vert > \vert \boldsymbol{a}_3\vert > \vert \boldsymbol{a}_2\vert`,
  then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (\boldsymbol{a}_2, \boldsymbol{a}_3, \boldsymbol{a}_1)

  and

  .. math::

    \boldsymbol{S} =
    \begin{pmatrix}
      0 & 1 & 0 \\
      0 & 0 & 1 \\
      1 & 0 & 0
    \end{pmatrix}
    \qquad
    \boldsymbol{S}^{-1}
    =
    \boldsymbol{S}^T
    =
    \begin{pmatrix}
      0 & 0 & 1 \\
      1 & 0 & 0 \\
      0 & 1 & 0
    \end{pmatrix}


* If :math:`\vert \boldsymbol{a}_1\vert > \vert \boldsymbol{a}_2\vert > \vert \boldsymbol{a}_3\vert`,
  then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (-\boldsymbol{a}_3, -\boldsymbol{a}_2, -\boldsymbol{a}_1)

  and

  .. math::

    \boldsymbol{S}
    =
    \boldsymbol{S}^{-1}
    =
    \boldsymbol{S}^T
    =
    \begin{pmatrix}
      0 & 0 & -1 \\
      0 & -1 & 0 \\
      -1 & 0 & 0
    \end{pmatrix}

.. note::

    All six changes of the cell preserve handiness of the original one.

Edge cases
==========
If :math:`a = b \ne c` or :math:`a = c \ne b` or :math:`b = c \ne a`,
then the lattice is :ref:`guide_tet`.

If :math:`a = b = c`, then the lattice is :ref:`guide_cub`.
