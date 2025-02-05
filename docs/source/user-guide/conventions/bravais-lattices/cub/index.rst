.. _guide_cub:

***********
Cubic (CUB)
***********

**Pearson symbol**: cP

**Constructor**:  :py:func:`.CUB`

It is defined by one parameter: :math:`a`. Standardized primitive and conventional cells
in the default orientation are

.. math::

    \begin{matrix}
    \boldsymbol{a}_1^s &=& \boldsymbol{a}_1^{cs} &=& (a, &0, &0)\\
    \boldsymbol{a}_2^s &=& \boldsymbol{a}_2^{cs} &=& (0, &a, &0)\\
    \boldsymbol{a}_3^s &=& \boldsymbol{a}_3^{cs} &=& (0, &0, &a)
    \end{matrix}

Transformation matrix from standardized primitive cell to standardized conventional cell is

.. include:: C_matrix.inc

K-path
======

:math:`\mathrm{\Gamma-X-M-\Gamma-R-X\vert M-R}`.

=======================  ================================  ================================  ================================
Point                    :math:`\times\boldsymbol{b}_1^s`  :math:`\times\boldsymbol{b}_2^s`  :math:`\times\boldsymbol{b}_3^s`
=======================  ================================  ================================  ================================
:math:`\mathrm{\Gamma}`  :math:`0`                         :math:`0`                         :math:`0`
:math:`\mathrm{M}`       :math:`1/2`                       :math:`1/2`                       :math:`0`
:math:`\mathrm{R}`       :math:`1/2`                       :math:`1/2`                       :math:`1/2`
:math:`\mathrm{X}`       :math:`0`                         :math:`1/2`                       :math:`0`
=======================  ================================  ================================  ================================

Variations
==========

There are no variations for cubic lattice.
One example is predefined: ``cub`` with :math:`a = \pi`.

Examples
========

Brillouin zone and default kpath
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: cub_brillouin.py
    :language: py

.. raw:: html
    :file: cub_brillouin.html

Primitive and conventional cell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: cub_real.py
    :language: py

.. raw:: html
    :file: cub_real.html

Wigner-Seitz cell
^^^^^^^^^^^^^^^^^
.. literalinclude:: cub_wigner-seitz.py
    :language: py

.. raw:: html
    :file: cub_wigner-seitz.html

Cell standardization
====================

No standardization required.

.. math::

    \boldsymbol{S}
    =
    \boldsymbol{S}^{-1}
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}
