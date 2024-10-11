.. _guide_mcl:

****************
Monoclinic (MCL)
****************

**Pearson symbol**: mP

**Constructor**:  :py:func:`.MCL`

It is defined by four parameter: :math:`a`, :math:`b`, :math:`c` and :math:`\alpha`
with primitive and conventional cell:

.. math::

    \begin{matrix}
    \boldsymbol{a}_1 &=& \boldsymbol{a}_1^c &=& (a, &0, &0)\\
    \boldsymbol{a}_2 &=& \boldsymbol{a}_2^c &=& (0, &b, &0)\\
    \boldsymbol{a}_3 &=& \boldsymbol{a}_3^c &=& (0, &c\cos\alpha, &c\sin\alpha)
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


Order of parameters: :math:`b \le c`, :math:`\alpha < 90^{\circ}`.


K-path
======

:math:`\mathrm{\Gamma-Y-H-C-E-M_1-A-X-H_1\vert M-D-Z\vert Y-D}`

.. math::

    \begin{matrix}
    \eta = \dfrac{1 - b\cos\alpha / c}{2\sin^2\alpha} &
    \nu = \dfrac{1}{2} - \dfrac{\eta c\cos\alpha}{b}
    \end{matrix}

=========================  ==============================  ==============================  ==============================
Point                      :math:`\times\boldsymbol{b}_1`  :math:`\times\boldsymbol{b}_2`  :math:`\times\boldsymbol{b}_3`
=========================  ==============================  ==============================  ==============================
:math:`\mathrm{\Gamma}`    :math:`0`                       :math:`0`                       :math:`0`
:math:`\mathrm{A}`         :math:`1/2`                     :math:`1/2`                     :math:`0`
:math:`\mathrm{C}`         :math:`0`                       :math:`1/2`                     :math:`1/2`
:math:`\mathrm{D}`         :math:`1/2`                     :math:`0`                       :math:`1/2`
:math:`\mathrm{D_1}`       :math:`1/2`                     :math:`0`                       :math:`-1/2`
:math:`\mathrm{E}`         :math:`1/2`                     :math:`1/2`                     :math:`1/2`
:math:`\mathrm{H}`         :math:`0`                       :math:`\eta`                    :math:`1-\nu`
:math:`\mathrm{H_1}`       :math:`0`                       :math:`1-\eta`                  :math:`\nu`
:math:`\mathrm{H_2}`       :math:`0`                       :math:`\eta`                    :math:`-\nu`
:math:`\mathrm{M}`         :math:`1/2`                     :math:`\eta`                    :math:`1-\nu`
:math:`\mathrm{M_1}`       :math:`1/2`                     :math:`1-\eta`                  :math:`\nu`
:math:`\mathrm{M_2}`       :math:`1/2`                     :math:`\eta`                    :math:`-\nu`
:math:`\mathrm{X}`         :math:`0`                       :math:`1/2`                     :math:`0`
:math:`\mathrm{Y}`         :math:`0`                       :math:`0`                       :math:`1/2`
:math:`\mathrm{Y_1}`       :math:`0`                       :math:`0`                       :math:`-1/2`
:math:`\mathrm{Z}`         :math:`1/2`                     :math:`0`                       :math:`0`
=========================  ==============================  ==============================  ==============================

Variations
==========

There are no variations for monoclinic lattice. One example is predefined: ``mcl`` with
:math:`a = \pi`, :math:`b = 1.3 \pi` :math:`c = 1.6 \pi` and :math:`\alpha = 75^{\circ}`.

Examples
========
Brillouin zone and default kpath
--------------------------------
.. literalinclude:: mcl_brillouin.py
    :language: py

.. raw:: html
    :file: mcl_brillouin.html

Primitive and conventional cell
-------------------------------
.. literalinclude:: mcl_real.py
    :language: py

.. raw:: html
    :file: mcl_real.html

Wigner-Seitz cell
-----------------
.. literalinclude:: mcl_wigner-seitz.py
    :language: py

.. raw:: html
    :file: mcl_wigner-seitz.html


Cell standardization
====================

Conditions :math:`b \le c` and :math:`\alpha < 90^{\circ}` are checked directly.
Matrix :math:`\boldsymbol{S}` is constructed in three steps.

Step 1
--------------------------------

* If :math:`\beta = \gamma = \frac{\pi}{2}` and :math:`\alpha \ne \frac{\pi}{2}`, then

  .. math::

    (\boldsymbol{a}_1^1, \boldsymbol{a}_2^1, \boldsymbol{a}_3^1)
    =
    (\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)

  and

  .. math::

    \boldsymbol{S}_1
    =
    \boldsymbol{S}_1^{-1}
    =
    \boldsymbol{S}_1^T
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}

* If :math:`\alpha = \gamma = \frac{\pi}{2}` and :math:`\beta \ne \frac{\pi}{2}`, then

  .. math::

    (\boldsymbol{a}_1^1, \boldsymbol{a}_2^1, \boldsymbol{a}_3^1)
    =
    (\boldsymbol{a}_2, \boldsymbol{a}_3, \boldsymbol{a}_1)

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
    \boldsymbol{S}_1^T
    =
    \begin{pmatrix}
      0 & 0 & 1 \\
      1 & 0 & 0 \\
      0 & 1 & 0
    \end{pmatrix}

* If :math:`\alpha = \beta = \frac{\pi}{2}` and :math:`\gamma \ne \frac{\pi}{2}`, then

  .. math::

    (\boldsymbol{a}_1^1, \boldsymbol{a}_2^1, \boldsymbol{a}_3^1)
    =
    (\boldsymbol{a}_3, \boldsymbol{a}_1, \boldsymbol{a}_2)

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
    \boldsymbol{S}_1^T
    =
    \begin{pmatrix}
      0 & 1 & 0 \\
      0 & 0 & 1 \\
      1 & 0 & 0
    \end{pmatrix}

Step 2
------
* If :math:`\vert \boldsymbol{a}_2^1 \vert  \le \vert \boldsymbol{a}_3^1 \vert`, then

  .. math::

    (\boldsymbol{a}_1^2, \boldsymbol{a}_2^2, \boldsymbol{a}_3^2)
    =
    (\boldsymbol{a}_1^1, \boldsymbol{a}_2^1, \boldsymbol{a}_3^1)

  and

  .. math::

    \boldsymbol{S}_2
    =
    \boldsymbol{S}_1
    \qquad
    \boldsymbol{S}_2^{-1}
    =
    \boldsymbol{S}_2^T
    =
    \boldsymbol{S}_1^{-1}
    =
    \boldsymbol{S}_1^T

* If :math:`\vert \boldsymbol{a}_2^1 \vert  > \vert \boldsymbol{a}_3^1 \vert`, then

  .. math::

    (\boldsymbol{a}_1^2, \boldsymbol{a}_2^2, \boldsymbol{a}_3^2)
    =
    (-\boldsymbol{a}_1^1, \boldsymbol{a}_3^1, \boldsymbol{a}_2^1)

  and

  .. math::

    \boldsymbol{S}_2
    =
    \begin{pmatrix}
      -1 & 0 & 0 \\
      0 & 0 & 1 \\
      0 & 1 & 0
    \end{pmatrix}
    \boldsymbol{S}_1
    \qquad
    \boldsymbol{S}_2^{-1}
    =
    \boldsymbol{S}_2^T
    =
    \boldsymbol{S}_1^{-1}
    \begin{pmatrix}
      -1 & 0 & 0 \\
      0 & 0 & 1 \\
      0 & 1 & 0
    \end{pmatrix}
    =
    \boldsymbol{S}_1^T
    \begin{pmatrix}
      -1 & 0 & 0 \\
      0 & 0 & 1 \\
      0 & 1 & 0
    \end{pmatrix}

Step 3
------

* If :math:`\alpha^2 < \frac{\pi}{2}`, then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (\boldsymbol{a}_1^2, \boldsymbol{a}_2^2, \boldsymbol{a}_3^2)

  and

  .. math::

    \boldsymbol{S}
    =
    \boldsymbol{S}_2\boldsymbol{S}_1
    \qquad
    \boldsymbol{S}^{-1}
    =
    \boldsymbol{S}^T
    =
    \boldsymbol{S}_1^{-1} \boldsymbol{S}_2^{-1}
    =
    \boldsymbol{S}_1^T \boldsymbol{S}_2^T

* If :math:`\alpha^2 > \frac{\pi}{2}`, then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s)
    =
    (-\boldsymbol{a}_1^2, -\boldsymbol{a}_2^2, \boldsymbol{a}_3^2)

  and

  .. math::

    \boldsymbol{S}
    =
    \begin{pmatrix}
      -1 & 0 & 0 \\
      0 & -1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}
    \boldsymbol{S}_2
    \boldsymbol{S}_1
    \qquad
    \boldsymbol{S}^{-1}
    =
    \boldsymbol{S}^T
    =
    \boldsymbol{S}_1^{-1} \boldsymbol{S}_2^{-1}
    \begin{pmatrix}
      -1 & 0 & 0 \\
      0 & -1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}
    =
    \boldsymbol{S}_1^T \boldsymbol{S}_2^T
    \begin{pmatrix}
      -1 & 0 & 0 \\
      0 & -1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}

.. note::

    All changes of the cell preserve handiness of the original one.

Edge cases
==========

If (:math:`\alpha = 60^{\circ}` or :math:`\alpha = 120^{\circ}`) and :math:`b = c`,
then the lattice is :ref:`guide_hex`.

If (:math:`\alpha = 30^{\circ}` or :math:`\alpha = 150^{\circ}`
or :math:`\alpha = 45^{\circ}` or :math:`\alpha = 145^{\circ}`) and :math:`b = c`,
then the lattice is :ref:`guide_orcc`.

If (:math:`\alpha = 60^{\circ}` or :math:`\alpha = 120^{\circ}`) and :math:`a \ne b = c/2`,
then the lattice is :ref:`guide_orc`.

If :math:`a \ne b \ne c` and :math:`\alpha = 90^{\circ}`, then the lattice is :ref:`guide_orc`.

If (:math:`\alpha = 60^{\circ}` or :math:`\alpha = 120^{\circ}`) and :math:`a = b = c/2`,
then the lattice is :ref:`guide_tet`.

If (:math:`a = b \ne c` or :math:`a = c \ne b` or :math:`b = c \ne a`) and :math:`\alpha = 90^{\circ}`, then the lattice is :ref:`guide_tet`.

If :math:`a = b = c` and :math:`\alpha = 90^{\circ}`, then the lattice is :ref:`guide_cub`.
