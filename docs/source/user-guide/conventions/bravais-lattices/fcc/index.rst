.. _guide_fcc:

************************
Face-centred cubic (FCC)
************************

**Pearson symbol**: cF

**Constructor**:  :py:func:`.FCC`

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
    \boldsymbol{a}_1 &=& (0, &a/2, &a/2)\\
    \boldsymbol{a}_2 &=& (a/2, &0, &a/2)\\
    \boldsymbol{a}_3 &=& (a/2, &a/2, &0)
    \end{matrix}

with

.. math::

    \boldsymbol{C}
    =
    \dfrac{1}{2}
    \begin{pmatrix}
      0 & 1 & 1 \\
      1 & 0 & 1 \\
      1 & 1 & 0
    \end{pmatrix}
    \qquad
    \boldsymbol{C}^{-1}
    =
    \begin{pmatrix}
      -1 & 1 & 1 \\
      1 & -1 & 1 \\
      1 & 1 & -1
    \end{pmatrix}

Variations
==========

There are no variations for face-centered cubic lattice.
One example is predefined: ``fcc`` with :math:`a = \pi`.

K-path
======

:math:`\mathrm{\Gamma-X-W-K-\Gamma-L-U-W-L-K\vert U-X}`

=======================  ==============================  ==============================  ==============================
Point                    :math:`\times\boldsymbol{b}_1`  :math:`\times\boldsymbol{b}_2`  :math:`\times\boldsymbol{b}_3`
=======================  ==============================  ==============================  ==============================
:math:`\mathrm{\Gamma}`  :math:`0`                       :math:`0`                       :math:`0`
:math:`\mathrm{K}`       :math:`3/8`                     :math:`3/8`                     :math:`3/4`
:math:`\mathrm{L}`       :math:`1/2`                     :math:`1/2`                     :math:`1/2`
:math:`\mathrm{U}`       :math:`5/8`                     :math:`1/4`                     :math:`5/8`
:math:`\mathrm{W}`       :math:`1/2`                     :math:`1/4`                     :math:`3/4`
:math:`\mathrm{X}`       :math:`1/2`                     :math:`0`                       :math:`1/2`
=======================  ==============================  ==============================  ==============================

Examples
========

Brillouin zone and default kpath
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: fcc_brillouin.py
    :language: py

.. raw:: html
    :file: fcc_brillouin.html

Primitive and conventional cell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: fcc_real.py
    :language: py

.. raw:: html
    :file: fcc_real.html

Wigner-Seitz cell
^^^^^^^^^^^^^^^^^
.. literalinclude:: fcc_wigner-seitz.py
    :language: py

.. raw:: html
    :file: fcc_wigner-seitz.html

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
