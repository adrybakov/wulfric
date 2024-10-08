.. _guide_hex:

***************
Hexagonal (HEX)
***************

**Pearson symbol**: hP

**Constructor**:  :py:func:`.HEX`

It is defined by two parameter: :math:`a` and :math:`c`
with primitive and conventional cell:

.. math::

    \begin{matrix}
    \boldsymbol{a}_1 &=& \boldsymbol{a}_1^c &=& (\frac{a}{2}, &\frac{-a\sqrt{3}}{2}, &0)\\
    \boldsymbol{a}_2 &=& \boldsymbol{a}_2^c &=& (\frac{a}{2}, &\frac{a\sqrt{3}}{2}, &0)\\
    \boldsymbol{a}_3 &=& \boldsymbol{a}_3^c &=& (0, &0, &c)
    \end{matrix}

with

.. math::

    \boldsymbol{C}
    =
    \boldsymbol{C}^{-1}
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}

K-path
======

:math:`\mathrm{\Gamma-M-K-\Gamma-A-L-H-A\vert L-M\vert K-H}`

=========================  ==============================  ==============================  ==============================
Point                      :math:`\times\boldsymbol{b}_1`  :math:`\times\boldsymbol{b}_2`  :math:`\times\boldsymbol{b}_3`
=========================  ==============================  ==============================  ==============================
:math:`\mathrm{\Gamma}`    :math:`0`                       :math:`0`                       :math:`0`
:math:`\mathrm{A}`         :math:`0`                       :math:`0`                       :math:`1/2`
:math:`\mathrm{H}`         :math:`1/3`                     :math:`1/3`                     :math:`1/2`
:math:`\mathrm{K}`         :math:`1/3`                     :math:`1/3`                     :math:`0`
:math:`\mathrm{L}`         :math:`1/2`                     :math:`0`                       :math:`1/2`
:math:`\mathrm{M}`         :math:`1/2`                     :math:`0`                       :math:`0`
=========================  ==============================  ==============================  ==============================

Variations
==========

There are no variations for hexagonal lattice.
One example is predefined: ``hex`` with :math:`a = \pi` and :math:`c = 2\pi`.

Examples
========

Brillouin zone and default kpath
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: hex_brillouin.py
    :language: py

.. raw:: html
    :file: hex_brillouin.html

Primitive and conventional cell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: hex_real.py
    :language: py

.. raw:: html
    :file: hex_real.html

Wigner-Seitz cell
^^^^^^^^^^^^^^^^^
.. literalinclude:: hex_wigner-seitz.py
    :language: py

.. raw:: html
    :file: hex_wigner-seitz.html


Cell standardization
====================

Since parameters :math:`a` and :math:`c` are not restricted (i.e. :math:`a = c` is
allowed), we use angles :math:`\alpha`, :math:`\beta` and :math:`\gamma` to
determine the standard form of the cell. For the primitive cell in a standard form
:math:`\alpha = \beta = 90^{\circ}` and :math:`\gamma = 120^{\circ}`. In practice these
conditions are equivalent to :math:`\boldsymbol{a}_2 \cdot \boldsymbol{a}_3 = \boldsymbol{a}_1 \cdot \boldsymbol{a}_3 = 0`
and :math:`\boldsymbol{a}_1 \cdot \boldsymbol{a}_2 < 0`.

* If :math:`\alpha = \beta = \pi` and :math:`\gamma = \frac{2\pi}{3}` (i.e.
  :math:`\boldsymbol{a}_2 \cdot \boldsymbol{a}_3 = \boldsymbol{a}_1 \cdot \boldsymbol{a}_3 = 0`
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

* If :math:`\beta = \gamma = \pi` and :math:`\alpha = \frac{2\pi}{3}` (i.e.
  :math:`\boldsymbol{a}_1 \cdot \boldsymbol{a}_3 = \boldsymbol{a}_1 \cdot \boldsymbol{a}_2 = 0`
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

* If :math:`\alpha = \gamma = \pi` and :math:`\beta = \frac{2\pi}{3}` (i.e.
  :math:`\boldsymbol{a}_2 \cdot \boldsymbol{a}_3 = \boldsymbol{a}_1 \cdot \boldsymbol{a}_2 = 0`
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
