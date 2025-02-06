.. _guide_tet:

****************
Tetragonal (TET)
****************

**Pearson symbol**: tP

**Constructor**:  :py:func:`.TET`

It is defined by two parameters :math:`a` and :math:`c` with :math:`a \ne c`.
Standardized primitive and conventional cells in the default orientation are

.. math::

  \begin{matrix}
  \boldsymbol{a}_1^s &=& \boldsymbol{a}_1^{cs} &=& (a, &0, &0)\\
  \boldsymbol{a}_2^s &=& \boldsymbol{a}_2^{cs} &=& (0, &a, &0)\\
  \boldsymbol{a}_3^s &=& \boldsymbol{a}_3^{cs} &=& (0, &0, &c)
  \end{matrix}

Transformation matrix from standardized primitive cell to standardized conventional cell
is

.. include:: C_matrix.inc

K-path
======

:math:`\mathrm{\Gamma-X-M-\Gamma-Z-R-A-Z\vert X-R\vert M-A}`

=======================  ================================  ================================  ================================
Point                    :math:`\times\boldsymbol{b}_1^s`  :math:`\times\boldsymbol{b}_2^s`  :math:`\times\boldsymbol{b}_3^s`
=======================  ================================  ================================  ================================
:math:`\mathrm{\Gamma}`  :math:`0`                         :math:`0`                         :math:`0`
:math:`\mathrm{A}`       :math:`1/2`                       :math:`1/2`                       :math:`1/2`
:math:`\mathrm{M}`       :math:`1/2`                       :math:`1/2`                       :math:`0`
:math:`\mathrm{R}`       :math:`0`                         :math:`1/2`                       :math:`1/2`
:math:`\mathrm{X}`       :math:`0`                         :math:`1/2`                       :math:`0`
:math:`\mathrm{Z}`       :math:`0`                         :math:`0`                         :math:`1/2`
=======================  ================================  ================================  ================================

Variations
==========

There are no variations for tetragonal lattice.
One example is predefined: ``tet`` with :math:`a = \pi` and :math:`c = 1.5\pi`

Examples
========

Brillouin zone and default kpath
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: tet_brillouin.py
    :language: py

.. raw:: html
    :file: tet_brillouin.html

Primitive and conventional cell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: tet_real.py
    :language: py

.. raw:: html
    :file: tet_real.html

Wigner-Seitz cell
^^^^^^^^^^^^^^^^^
.. literalinclude:: tet_wigner-seitz.py
    :language: py

.. raw:: html
    :file: tet_wigner-seitz.html

Cell standardization
====================

Length of third lattice vector has to be different from the first two.
If this condition is not satisfied,
then the lattice is transformed to the standard form:


* If
  :math:`\vert\boldsymbol{a}_1\vert = \vert\boldsymbol{a}_2\vert \ne \vert\boldsymbol{a}_3\vert`,
  then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)

  and

  .. math::

    \boldsymbol{S}
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}
    \qquad
    \boldsymbol{S}^{-1}
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}

* If
  :math:`\vert\boldsymbol{a}_2\vert = \vert\boldsymbol{a}_3\vert \ne \vert\boldsymbol{a}_1\vert`,
  then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (\boldsymbol{a}_2, \boldsymbol{a}_3, \boldsymbol{a}_1)

  and

  .. math::

    \boldsymbol{S}
    =
    \begin{pmatrix}
      0 & 0 & 1 \\
      1 & 0 & 0 \\
      0 & 1 & 0
    \end{pmatrix}
    \qquad
    \boldsymbol{S}^{-1}
    =
    \begin{pmatrix}
      0 & 1 & 0 \\
      0 & 0 & 1 \\
      1 & 0 & 0
    \end{pmatrix}

* If
  :math:`\vert\boldsymbol{a}_1\vert = \vert\boldsymbol{a}_3\vert \ne \vert\boldsymbol{a}_2\vert`,
  then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (\boldsymbol{a}_3, \boldsymbol{a}_1, \boldsymbol{a}_2)

  and

  .. math::

    \boldsymbol{S}
    =
    \begin{pmatrix}
      0 & 1 & 0 \\
      0 & 0 & 1 \\
      1 & 0 & 0
    \end{pmatrix}
    \qquad
    \boldsymbol{S}^{-1}
    =
    \begin{pmatrix}
      0 & 0 & 1 \\
      1 & 0 & 0 \\
      0 & 1 & 0
    \end{pmatrix}

Edge cases
==========

If :math:`a = c`, then the lattice is :ref:`guide_cub`.
