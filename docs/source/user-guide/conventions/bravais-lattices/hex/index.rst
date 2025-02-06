.. _guide_hex:

***************
Hexagonal (HEX)
***************

**Pearson symbol**: hP

**Constructor**:  :py:func:`.HEX`

It is defined by two parameters :math:`a` and :math:`c`. Standardized primitive and
conventional cells in the default orientation are

.. math::

  \begin{matrix}
    \boldsymbol{a}_1^s &=& \boldsymbol{a}_1^{cs} &=& (\frac{a}{2}, &\frac{-a\sqrt{3}}{2}, &0)\\
    \boldsymbol{a}_2^s &=& \boldsymbol{a}_2^{cs} &=& (\frac{a}{2}, &\frac{a\sqrt{3}}{2}, &0)\\
    \boldsymbol{a}_3^s &=& \boldsymbol{a}_3^{cs} &=& (0, &0, &c)
  \end{matrix}

Transformation matrix from standardized primitive cell to standardized conventional cell
is

.. include:: C_matrix.inc

K-path
======

:math:`\mathrm{\Gamma-M-K-\Gamma-A-L-H-A\vert L-M\vert K-H}`

=========================  ================================  ================================  ================================
Point                      :math:`\times\boldsymbol{b}_1^s`  :math:`\times\boldsymbol{b}_2^s`  :math:`\times\boldsymbol{b}_3^s`
=========================  ================================  ================================  ================================
:math:`\mathrm{\Gamma}`    :math:`0`                         :math:`0`                         :math:`0`
:math:`\mathrm{A}`         :math:`0`                         :math:`0`                         :math:`1/2`
:math:`\mathrm{H}`         :math:`1/3`                       :math:`1/3`                       :math:`1/2`
:math:`\mathrm{K}`         :math:`1/3`                       :math:`1/3`                       :math:`0`
:math:`\mathrm{L}`         :math:`1/2`                       :math:`0`                         :math:`1/2`
:math:`\mathrm{M}`         :math:`1/2`                       :math:`0`                         :math:`0`
=========================  ================================  ================================  ================================

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
allowed), wulfric uses angles :math:`\alpha`, :math:`\beta` and :math:`\gamma` to
determine the standard form of the cell. For the primitive cell in a standard form
:math:`\alpha^s = \beta^s = 90^{\circ}` and :math:`\gamma^s = 120^{\circ}`.

Matrix :math:`\boldsymbol{S}` is constructed in two steps.

Step 1
^^^^^^

* If :math:`\alpha = \beta = \dfrac{\pi}{2}` then

  .. math::

    (\boldsymbol{a}_1^{(1)}, \boldsymbol{a}_2^{(1)}, \boldsymbol{a}_3^{(1)})
    =
    (\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)

  and

  .. math::

    \boldsymbol{S}_1
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}
    \qquad
    \boldsymbol{S}_1^{-1}
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}

* If :math:`\beta = \gamma = \dfrac{\pi}{2}` then

  .. math::

    (\boldsymbol{a}_1^{(1)}, \boldsymbol{a}_2^{(1)}, \boldsymbol{a}_3^{(1)})
    =
    (\boldsymbol{a}_2, \boldsymbol{a}_3, \boldsymbol{a}_1)

  and

  .. math::

    \boldsymbol{S}_1
    =
    \begin{pmatrix}
      0 & 0 & 1 \\
      1 & 0 & 0 \\
      0 & 1 & 0
    \end{pmatrix}
    \qquad
    \boldsymbol{S}_1^{-1}
    =
    \begin{pmatrix}
      0 & 1 & 0 \\
      0 & 0 & 1 \\
      1 & 0 & 0
    \end{pmatrix}

* If :math:`\alpha = \gamma = \dfrac{\pi}{2}` then

  .. math::

    (\boldsymbol{a}_1^{(1)}, \boldsymbol{a}_2^{(1)}, \boldsymbol{a}_3^{(1)})
    =
    (\boldsymbol{a}_3, \boldsymbol{a}_1, \boldsymbol{a}_2)

  and

  .. math::

    \boldsymbol{S}_1
    =
    \begin{pmatrix}
      0 & 1 & 0 \\
      0 & 0 & 1 \\
      1 & 0 & 0
    \end{pmatrix}
    \qquad
    \boldsymbol{S}_1^{-1}
    =
    \begin{pmatrix}
      0 & 0 & 1 \\
      1 & 0 & 0 \\
      0 & 1 & 0
    \end{pmatrix}

Step 2
^^^^^^

* If :math:`\gamma^{(1)} =  \dfrac{2}{3}\pi` then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (\boldsymbol{a}_1^{(1)}, \boldsymbol{a}_2^{(1)}, \boldsymbol{a}_3^{(1)})

  and

  .. math::

    \boldsymbol{S}_2
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}
    \qquad
    \boldsymbol{S}_2^{-1}
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}

* If :math:`\gamma^{(1)} =  \dfrac{\pi}{3}` then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (\boldsymbol{a}_2^{(1)}, -\boldsymbol{a}_1^{(1)}, \boldsymbol{a}_3^{(1)})

  and

  .. math::

    \boldsymbol{S}_2
    =
    \begin{pmatrix}
      0 & -1 & 0 \\
      1 &  0 & 0 \\
      0 &  0 & 1
    \end{pmatrix}
    \qquad
    \boldsymbol{S}_2^{-1}
    =
    \begin{pmatrix}
      0  & 1 & 0 \\
      -1 & 0 & 0 \\
      0  & 0 & 1
    \end{pmatrix}

Finally
^^^^^^^
.. math::

    \boldsymbol{S}
    =
    \boldsymbol{S}_1 \boldsymbol{S}_2
    \qquad
    \boldsymbol{S}^{-1}
    =
    \boldsymbol{S}_2^{-1} \boldsymbol{S}_1^{-1}
