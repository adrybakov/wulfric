.. _guide_cub:

***********
Cubic (CUB)
***********

**Pearson symbol**: cP

**Constructor**:  :py:func:`.CUB`

It is defined by one parameter: :math:`a` with primitive and conventional cell:

.. math::

    \begin{matrix}
    \boldsymbol{a}_1 &=& \boldsymbol{a}_1^c &=& (a, &0, &0)\\
    \boldsymbol{a}_2 &=& \boldsymbol{a}_2^c &=& (0, &a, &0)\\
    \boldsymbol{a}_3 &=& \boldsymbol{a}_3^c &=& (0, &0, &a)
    \end{matrix}

with

.. math::

    \boldsymbol{C}
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}
    \qquad
    \boldsymbol{C}^{-1}
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}

Variations
==========

There are no variations for cubic lattice.
One example is predefined: ``cub`` with :math:`a = \pi`.

K-path
======

:math:`\mathrm{\Gamma-X-M-\Gamma-R-X\vert M-R}`.

=======================  ==============================  ==============================  ==============================
Point                    :math:`\times\boldsymbol{b}_1`  :math:`\times\boldsymbol{b}_2`  :math:`\times\boldsymbol{b}_3`
=======================  ==============================  ==============================  ==============================
:math:`\mathrm{\Gamma}`  :math:`0`                       :math:`0`                       :math:`0`
:math:`\mathrm{M}`       :math:`1/2`                     :math:`1/2`                     :math:`0`
:math:`\mathrm{R}`       :math:`1/2`                     :math:`1/2`                     :math:`1/2`
:math:`\mathrm{X}`       :math:`0`                       :math:`1/2`                     :math:`0`
=======================  ==============================  ==============================  ==============================

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
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}
