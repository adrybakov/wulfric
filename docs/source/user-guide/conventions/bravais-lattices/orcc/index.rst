.. _guide_orcc:

********************************
Base-centred orthorhombic (ORCC)
********************************

**Pearson symbol**: oS

**Constructor**:  :py:func:`.ORCC`

It is defined by three parameters :math:`a`, :math:`b` and :math:`c` with
:math:`a < b`. Standardized primitive and conventional cells in the default
orientation are

.. math::

  \begin{matrix}
    \boldsymbol{a}_1^s &=& (a/2, &-b/2, &0)\\
    \boldsymbol{a}_2^s &=& (a/2, &b/2, &0)\\
    \boldsymbol{a}_3^s &=& (0, &0, &c)
  \end{matrix}

.. math::

  \begin{matrix}
    \boldsymbol{a}_1^{cs} &=& (a, &0, &0)\\
    \boldsymbol{a}_2^{cs} &=& (0, &b, &0)\\
    \boldsymbol{a}_3^{cs} &=& (0, &0, &c)
  \end{matrix}

Transformation matrix from standardized primitive cell to standardized conventional cell
is

.. include:: C_matrix.inc


K-path
======

:math:`\mathrm{\Gamma-X-S-R-A-Z-\Gamma-Y-X_1-A_1-T-Y\vert Z-T}`

.. math::

  \zeta = \dfrac{1 + a^2/b^2}{4}

=========================  ================================  ================================  ================================
Point                      :math:`\times\boldsymbol{b}_1^s`  :math:`\times\boldsymbol{b}_2^s`  :math:`\times\boldsymbol{b}_3^s`
=========================  ================================  ================================  ================================
:math:`\mathrm{\Gamma}`    :math:`0`                         :math:`0`                         :math:`0`
:math:`\mathrm{A}`         :math:`\zeta`                     :math:`\zeta`                     :math:`1/2`
:math:`\mathrm{A_1}`       :math:`-\zeta`                    :math:`1-\zeta`                   :math:`1/2`
:math:`\mathrm{R}`         :math:`0`                         :math:`1/2`                       :math:`1/2`
:math:`\mathrm{S}`         :math:`0`                         :math:`1/2`                       :math:`0`
:math:`\mathrm{T}`         :math:`-1/2`                      :math:`1/2`                       :math:`1/2`
:math:`\mathrm{X}`         :math:`\zeta`                     :math:`\zeta`                     :math:`0`
:math:`\mathrm{X_1}`       :math:`-\zeta`                    :math:`1-\zeta`                   :math:`0`
:math:`\mathrm{Y}`         :math:`-1/2`                      :math:`1/2`                       :math:`0`
:math:`\mathrm{Z}`         :math:`0`                         :math:`0`                         :math:`1/2`
=========================  ================================  ================================  ================================


Variations
==========

There are no variations for base-centered orthorombic.
One example is predefined: ``orcc`` with
:math:`a = \pi`, :math:`b  = 1.3\pi` and :math:`c = 1.7\pi`.

Examples
========

Brillouin zone and default kpath
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: orcc_brillouin.py
    :language: py

.. raw:: html
    :file: orcc_brillouin.html

Primitive and conventional cell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: orcc_real.py
    :language: py

.. raw:: html
    :file: orcc_real.html

Wigner-Seitz cell
^^^^^^^^^^^^^^^^^
.. literalinclude:: orcc_wigner-seitz.py
    :language: py

.. raw:: html
    :file: orcc_wigner-seitz.html



Cell standardization
====================

Length of third vector of the primitive cell has to be different from
the lengths of the first two vectors of the primitive cell. Together with the
:math:`a < b` we arrive at the following condition of the angles of the primitive cell in
a standard form: :math:`\alpha = \beta = 90^{\circ}` and :math:`\gamma > 90^{\circ}`.
In practice this condition simplifies to
:math:`\boldsymbol{a}_2 \cdot \boldsymbol{a}_3 = \boldsymbol{a}_1 \cdot \boldsymbol{a}_3  = 0`
and
:math:`\boldsymbol{a}_1 \cdot \boldsymbol{a}_2 < 0`. We use angles of the primitive cell
for standardization.

* If :math:`\alpha = \beta = \frac{\pi}{2}` and :math:`\gamma > \frac{\pi}{2}` (i.e.
  :math:`\boldsymbol{a}_2 \cdot \boldsymbol{a}_3 = \boldsymbol{a}_1 \cdot \boldsymbol{a}_3  = 0`
  and
  :math:`\boldsymbol{a}_1 \cdot \boldsymbol{a}_2 < 0`),
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

* If :math:`\alpha = \beta = \frac{\pi}{2}` and :math:`\gamma < \frac{\pi}{2}` (i.e.
  :math:`\boldsymbol{a}_2 \cdot \boldsymbol{a}_3 = \boldsymbol{a}_1 \cdot \boldsymbol{a}_3  = 0`
  and
  :math:`\boldsymbol{a}_1 \cdot \boldsymbol{a}_2 > 0`),
  then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (\boldsymbol{a}_2, -\boldsymbol{a}_1, \boldsymbol{a}_3)

  and

  .. math::

    \boldsymbol{S}
    =
    \begin{pmatrix}
      0 & 1 & 0 \\
      -1 & 0 & 0 \\
      0 & 0 & 1
    \end{pmatrix}
    \qquad
    \boldsymbol{S}^{-1}
    =
    \boldsymbol{S}^T
    =
    \begin{pmatrix}
      0 & -1 & 0 \\
      1 & 0 & 0 \\
      0 & 0 & 1
    \end{pmatrix}

* If :math:`\beta = \gamma = \frac{\pi}{2}` and :math:`\alpha > \frac{\pi}{2}` (i.e.
  :math:`\boldsymbol{a}_1 \cdot \boldsymbol{a}_3 = \boldsymbol{a}_1 \cdot \boldsymbol{a}_2  = 0`
  and
  :math:`\boldsymbol{a}_2 \cdot \boldsymbol{a}_3 < 0`),
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

* If :math:`\beta = \gamma = \frac{\pi}{2}` and :math:`\alpha < \frac{\pi}{2}` (i.e.
  :math:`\boldsymbol{a}_1 \cdot \boldsymbol{a}_3 = \boldsymbol{a}_1 \cdot \boldsymbol{a}_2  = 0`
  and
  :math:`\boldsymbol{a}_2 \cdot \boldsymbol{a}_3 > 0`),
  then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (\boldsymbol{a}_3, -\boldsymbol{a}_2, \boldsymbol{a}_1)

  and

  .. math::

    \boldsymbol{S}
    =
    \boldsymbol{S}^{-1}
    =
    \boldsymbol{S}^T
    =
    \begin{pmatrix}
      0 & 0 & 1 \\
      0 & -1 & 0 \\
      1 & 0 & 0
    \end{pmatrix}

* If :math:`\alpha = \gamma = \frac{\pi}{2}` and :math:`\beta > \frac{\pi}{2}` (i.e.
  :math:`\boldsymbol{a}_2 \cdot \boldsymbol{a}_3 = \boldsymbol{a}_1 \cdot \boldsymbol{a}_2  = 0`
  and
  :math:`\boldsymbol{a}_1 \cdot \boldsymbol{a}_3 < 0`),
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

* If :math:`\alpha = \gamma = \frac{\pi}{2}` and :math:`\beta < \frac{\pi}{2}` (i.e.
  :math:`\boldsymbol{a}_2 \cdot \boldsymbol{a}_3 = \boldsymbol{a}_1 \cdot \boldsymbol{a}_2  = 0`
  and
  :math:`\boldsymbol{a}_1 \cdot \boldsymbol{a}_3 > 0`),
  then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (\boldsymbol{a}_1, -\boldsymbol{a}_3, \boldsymbol{a}_2)

  and

  .. math::

    \boldsymbol{S}
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 0 & -1 \\
      0 & 1 & 0
    \end{pmatrix}
    \qquad
    \boldsymbol{S}^{-1}
    =
    \boldsymbol{S}^T
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 0 & 1 \\
      0 & -1 & 0
    \end{pmatrix}

.. note::

    All six changes of the cell preserve handiness of the original one.


Edge cases
==========
If :math:`a = b`, then the lattice is :ref:`guide_tet`.

If :math:`a = b = \sqrt{2} c`, then the lattice is :ref:`guide_cub`.
