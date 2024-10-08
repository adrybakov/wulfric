.. _guide_bcc:

*************************
Body-centered cubic (BCC)
*************************

**Pearson symbol**: cI

**Constructor**:  :py:func:`.BCC`

It is defined by one parameter: :math:`a` with conventional cell:

.. math::

    \begin{matrix}
    \boldsymbol{a}_1^c &=& (a, &0, &0)\\
    \boldsymbol{a}_2^c &=& (0, &a, &0)\\
    \boldsymbol{a}_3^c &=& (0, &0, &a)
    \end{matrix}

And primitive cell:

.. math::

    \begin{matrix}
    \boldsymbol{a}_1 &=& (-a/2,& a/2,& a/2)\\
    \boldsymbol{a}_2 &=& (a/2, &-a/2,& a/2)\\
    \boldsymbol{a}_3 &=& (a/2, &a/2, &-a/2)
    \end{matrix}

with

.. math::

    \boldsymbol{C}
    =
    \dfrac{1}{2}
    \begin{pmatrix}
      -1 & 1 & 1 \\
      1 & -1 & 1 \\
      1 & 1 & -1
    \end{pmatrix}
    \qquad
    \boldsymbol{C}^{-1}
    =
    \begin{pmatrix}
      0 & 1 & 1 \\
      1 & 0 & 1 \\
      1 & 1 & 0
    \end{pmatrix}

K-path
======

:math:`\mathrm{\Gamma-H-N-\Gamma-P-H\vert P-N}`

=======================  ==============================  ==============================  ==============================
Point                    :math:`\times\boldsymbol{b}_1`  :math:`\times\boldsymbol{b}_2`  :math:`\times\boldsymbol{b}_3`
=======================  ==============================  ==============================  ==============================
:math:`\mathrm{\Gamma}`  :math:`0`                       :math:`0`                       :math:`0`
:math:`\mathrm{H}`       :math:`1/2`                     :math:`-1/2`                    :math:`1/2`
:math:`\mathrm{P}`       :math:`1/4`                     :math:`1/4`                     :math:`1/4`
:math:`\mathrm{N}`       :math:`0`                       :math:`0`                       :math:`1/2`
=======================  ==============================  ==============================  ==============================

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
