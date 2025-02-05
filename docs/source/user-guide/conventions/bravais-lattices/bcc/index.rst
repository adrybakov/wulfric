.. _guide_bcc:

*************************
Body-centered cubic (BCC)
*************************

**Pearson symbol**: cI

**Constructor**:  :py:func:`.BCC`

It is defined by one parameters :math:`a`. Standardized primitive and conventional cells
in the default orientation are

.. math::

    \begin{matrix}
    \boldsymbol{a}_1^s &=& (-a/2,& a/2,& a/2)\\
    \boldsymbol{a}_2^s &=& (a/2, &-a/2,& a/2)\\
    \boldsymbol{a}_3^s &=& (a/2, &a/2, &-a/2)
    \end{matrix}

.. math::

    \begin{matrix}
    \boldsymbol{a}_1^{cs} &=& (a, &0, &0)\\
    \boldsymbol{a}_2^{cs} &=& (0, &a, &0)\\
    \boldsymbol{a}_3^{cs} &=& (0, &0, &a)
    \end{matrix}

Transformation matrix from standardized primitive cell to standardized conventional cell
is

.. include:: C_matrix.inc

K-path
======

:math:`\mathrm{\Gamma-H-N-\Gamma-P-H\vert P-N}`

=======================  ================================  ================================  ================================
Point                    :math:`\times\boldsymbol{b}_1^s`  :math:`\times\boldsymbol{b}_2^s`  :math:`\times\boldsymbol{b}_3^s`
=======================  ================================  ================================  ================================
:math:`\mathrm{\Gamma}`  :math:`0`                         :math:`0`                         :math:`0`
:math:`\mathrm{H}`       :math:`1/2`                       :math:`-1/2`                      :math:`1/2`
:math:`\mathrm{P}`       :math:`1/4`                       :math:`1/4`                       :math:`1/4`
:math:`\mathrm{N}`       :math:`0`                         :math:`0`                         :math:`1/2`
=======================  ================================  ================================  ================================

Variations
==========

There are no variations for body-centered cubic lattice.
One example is predefined: ``bcc`` with :math:`a = \pi`.

Examples
========

Brillouin zone and default kpath
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: bcc_brillouin.py
    :language: py

.. raw:: html
    :file: bcc_brillouin.html


Primitive and conventional cell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: bcc_real.py
    :language: py

.. raw:: html
    :file: bcc_real.html

Wigner-Seitz cell
^^^^^^^^^^^^^^^^^
.. literalinclude:: bcc_wigner-seitz.py
    :language: py

.. raw:: html
    :file: bcc_wigner-seitz.html

Cell standardization
====================

No standardization required.

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
