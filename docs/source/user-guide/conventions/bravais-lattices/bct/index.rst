.. _guide_bct:

*****************************
Body-centred tetragonal (BCT)
*****************************

**Pearson symbol**: tI

**Constructor**:  :py:func:`.BCT`

It is defined by two parameters :math:`a` and :math:`c` with :math:`a \ne c`.
Standardized primitive and conventional cells in the default orientation are

.. math::

    \begin{matrix}
    \boldsymbol{a}_1^s &=& (-a/2, &a/2, &c/2)\\
    \boldsymbol{a}_2^s &=& (a/2, &-a/2, &c/2)\\
    \boldsymbol{a}_3^s &=& (a/2, &a/2, &-c/2)
    \end{matrix}

.. math::

    \begin{matrix}
    \boldsymbol{a}_1^{cs} &=& (a, &0, &0)\\
    \boldsymbol{a}_2^{cs} &=& (0, &a, &0)\\
    \boldsymbol{a}_3^{cs} &=& (0, &0, &c)
    \end{matrix}

Transformation matrix from standardized primitive cell to standardized conventional cell
is

.. include:: C_matrix.inc


K-path
======

BCT\ :sub:`1`
-------------

:math:`\mathrm{\Gamma-X-M-\Gamma-Z-P-N-Z_1-M\vert X-P}`

.. math::

    \eta = \dfrac{1 + c^2/a^2}{4}

=======================  ================================  ================================  ================================
Point                    :math:`\times\boldsymbol{b}_1^s`  :math:`\times\boldsymbol{b}_2^s`  :math:`\times\boldsymbol{b}_3^s`
=======================  ================================  ================================  ================================
:math:`\mathrm{\Gamma}`  :math:`0`                         :math:`0`                         :math:`0`
:math:`\mathrm{M}`       :math:`-1/2`                      :math:`1/2`                       :math:`1/2`
:math:`\mathrm{N}`       :math:`0`                         :math:`1/2`                       :math:`0`
:math:`\mathrm{P}`       :math:`1/4`                       :math:`1/4`                       :math:`1/4`
:math:`\mathrm{X}`       :math:`0`                         :math:`0`                         :math:`1/2`
:math:`\mathrm{Z}`       :math:`\eta`                      :math:`\eta`                      :math:`-\eta`
:math:`\mathrm{Z}_1`     :math:`-\eta`                     :math:`1-\eta`                    :math:`\eta`
=======================  ================================  ================================  ================================

BCT\ :sub:`2`
-------------

:math:`\mathrm{\Gamma-X-Y-\Sigma-\Gamma-Z-\Sigma_1-N-P-Y_1-Z\vert X-P}`

.. math::

    \begin{matrix}
    \eta = \dfrac{1 + a^2/c^2}{4} &
    \zeta = \dfrac{a^2}{2c^2}
    \end{matrix}

=========================  ================================  ================================  ================================
Point                      :math:`\times\boldsymbol{b}_1^s`  :math:`\times\boldsymbol{b}_2^s`  :math:`\times\boldsymbol{b}_3^s`
=========================  ================================  ================================  ================================
:math:`\mathrm{\Gamma}`    :math:`0`                         :math:`0`                         :math:`0`
:math:`\mathrm{N}`         :math:`0`                         :math:`1/2`                       :math:`0`
:math:`\mathrm{P}`         :math:`1/4`                       :math:`1/4`                       :math:`1/4`
:math:`\mathrm{\Sigma}`    :math:`-\eta`                     :math:`\eta`                      :math:`\eta`
:math:`\mathrm{\Sigma_1}`  :math:`\eta`                      :math:`1-\eta`                    :math:`-\eta`
:math:`\mathrm{X}`         :math:`0`                         :math:`0`                         :math:`1/2`
:math:`\mathrm{Y}`         :math:`-\zeta`                    :math:`\zeta`                     :math:`1/2`
:math:`\mathrm{Y}_1`       :math:`1/2`                       :math:`1/2`                       :math:`-\zeta`
:math:`\mathrm{Z}`         :math:`1/2`                       :math:`1/2`                       :math:`-1/2`
=========================  ================================  ================================  ================================


Variations
==========

There are two variations of body-centered tetragonal lattice.

BCT\ :sub:`1`
-------------

:math:`c < a`.

Predefined example: ``bct1`` with :math:`a = 1.5\pi` and :math:`c = \pi`.

BCT\ :sub:`2`
-------------

:math:`c > a`.

Predefined example: ``bct2`` with :math:`a = \pi` and :math:`c = 1.5\pi`.


Examples
========

BCT\ :sub:`1`
-------------

Brillouin zone and default kpath
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: bct1_reciprocal.py
    :language: py

.. raw:: html
    :file: bct1_reciprocal.html

Primitive, Wigner-Seitz and conventional cells
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Click on the legend to hide a cell.

.. literalinclude:: bct1_real.py
    :language: py

.. raw:: html
    :file: bct1_real.html

BCT\ :sub:`2`
-------------


Brillouin zone and default kpath
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: bct2_reciprocal.py
    :language: py

.. raw:: html
    :file: bct2_reciprocal.html

Primitive, Wigner-Seitz and conventional cells
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Click on the legend to hide a cell.

.. literalinclude:: bct2_real.py
    :language: py

.. raw:: html
    :file: bct2_real.html


Cell standardization
====================

Condition :math:`a \ne c` result in the condition :math:`\alpha^s = \beta^s \ne \gamma^s`
for the primitive cell in a standard form. Therefore, wulfric uses angles of the primitive cell
for standardization.

* If
  :math:`\alpha = \beta \ne \gamma` then

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
  :math:`\beta = \gamma \ne \alpha` then

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
  :math:`\alpha = \gamma \ne \beta` then

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

If :math:`a = c` then the lattice is :ref:`guide_bcc`.
