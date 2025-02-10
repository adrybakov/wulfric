.. _guide_tri:

***************
Triclinic (TRI)
***************

**Pearson symbol**: aP

**Constructor**:  :py:func:`.TRI`

It is defined by six parameters :math:`a`, :math:`b`, :math:`c` and :math:`\alpha`,
:math:`\beta`, :math:`\gamma`. Standardized primitive and conventional cells in the
default orientation are

.. math::

  \begin{matrix}
    \boldsymbol{a}_1^s &=& \boldsymbol{a}_1^{cs} &=& (a, &0, &0)\\
    \boldsymbol{a}_2^s &=& \boldsymbol{a}_2^{cs} &=& (b\cos\gamma, &b\sin\gamma, &0)\\
    \boldsymbol{a}_3^s &=& \boldsymbol{a}_3^{cs} &=& (c\cos\beta, &\dfrac{c(\cos\alpha - \cos\beta\cos\gamma)}{\sin\gamma}, &\dfrac{c}{\sin\gamma}\sqrt{\sin^2\gamma - \cos^2\alpha - \cos^2\beta + 2\cos\alpha\cos\beta\cos\gamma})
  \end{matrix}

Transformation matrix from standardized primitive cell to standardized conventional cell
is

.. include:: C_matrix.inc


K-path
======

TRI\ :sub:`1a`
--------------

:math:`\mathrm{X-\Gamma-Y\vert L-\Gamma-Z\vert N-\Gamma-M\vert R-\Gamma}`

=======================  ================================  ================================  ================================
Point                    :math:`\times\boldsymbol{b}_1^s`  :math:`\times\boldsymbol{b}_2^s`  :math:`\times\boldsymbol{b}_3^s`
=======================  ================================  ================================  ================================
:math:`\mathrm{\Gamma}`  :math:`0`                         :math:`0`                         :math:`0`
:math:`\mathrm{L}`       :math:`1/2`                       :math:`1/2`                       :math:`0`
:math:`\mathrm{M}`       :math:`0`                         :math:`1/2`                       :math:`1/2`
:math:`\mathrm{N}`       :math:`1/2`                       :math:`0`                         :math:`1/2`
:math:`\mathrm{R}`       :math:`1/2`                       :math:`1/2`                       :math:`1/2`
:math:`\mathrm{X}`       :math:`1/2`                       :math:`0`                         :math:`0`
:math:`\mathrm{Y}`       :math:`0`                         :math:`1/2`                       :math:`0`
:math:`\mathrm{Z}`       :math:`0`                         :math:`0`                         :math:`1/2`
=======================  ================================  ================================  ================================

TRI\ :sub:`2a`
--------------

:math:`\mathrm{X-\Gamma-Y\vert L-\Gamma-Z\vert N-\Gamma-M\vert R-\Gamma}`

=======================  ================================  ================================  ================================
Point                    :math:`\times\boldsymbol{b}_1^s`  :math:`\times\boldsymbol{b}_2^s`  :math:`\times\boldsymbol{b}_3^s`
=======================  ================================  ================================  ================================
:math:`\mathrm{\Gamma}`  :math:`0`                         :math:`0`                         :math:`0`
:math:`\mathrm{L}`       :math:`1/2`                       :math:`1/2`                       :math:`0`
:math:`\mathrm{M}`       :math:`0`                         :math:`1/2`                       :math:`1/2`
:math:`\mathrm{N}`       :math:`1/2`                       :math:`0`                         :math:`1/2`
:math:`\mathrm{R}`       :math:`1/2`                       :math:`1/2`                       :math:`1/2`
:math:`\mathrm{X}`       :math:`1/2`                       :math:`0`                         :math:`0`
:math:`\mathrm{Y}`       :math:`0`                         :math:`1/2`                       :math:`0`
:math:`\mathrm{Z}`       :math:`0`                         :math:`0`                         :math:`1/2`
=======================  ================================  ================================  ================================

TRI\ :sub:`1b`
--------------

:math:`\mathrm{X-\Gamma-Y\vert L-\Gamma-Z\vert N-\Gamma-M\vert R-\Gamma}`

=======================  ================================  ================================  ================================
Point                    :math:`\times\boldsymbol{b}_1^s`  :math:`\times\boldsymbol{b}_2^s`  :math:`\times\boldsymbol{b}_3^s`
=======================  ================================  ================================  ================================
:math:`\mathrm{\Gamma}`  :math:`0`                         :math:`0`                         :math:`0`
:math:`\mathrm{L}`       :math:`1/2`                       :math:`-1/2`                      :math:`0`
:math:`\mathrm{M}`       :math:`0`                         :math:`0`                         :math:`1/2`
:math:`\mathrm{N}`       :math:`-1/2`                      :math:`-1/2`                      :math:`1/2`
:math:`\mathrm{R}`       :math:`0`                         :math:`-1/2`                      :math:`1/2`
:math:`\mathrm{X}`       :math:`0`                         :math:`-1/2`                      :math:`0`
:math:`\mathrm{Y}`       :math:`1/2`                       :math:`0`                         :math:`0`
:math:`\mathrm{Z}`       :math:`-1/2`                      :math:`0`                         :math:`1/2`
=======================  ================================  ================================  ================================

TRI\ :sub:`2b`
--------------

:math:`\mathrm{X-\Gamma-Y\vert L-\Gamma-Z\vert N-\Gamma-M\vert R-\Gamma}`

=======================  ================================  ================================  ================================
Point                    :math:`\times\boldsymbol{b}_1^s`  :math:`\times\boldsymbol{b}_2^s`  :math:`\times\boldsymbol{b}_3^s`
=======================  ================================  ================================  ================================
:math:`\mathrm{\Gamma}`  :math:`0`                         :math:`0`                         :math:`0`
:math:`\mathrm{L}`       :math:`1/2`                       :math:`-1/2`                      :math:`0`
:math:`\mathrm{M}`       :math:`0`                         :math:`0`                         :math:`1/2`
:math:`\mathrm{N}`       :math:`-1/2`                      :math:`-1/2`                      :math:`1/2`
:math:`\mathrm{R}`       :math:`0`                         :math:`-1/2`                      :math:`1/2`
:math:`\mathrm{X}`       :math:`0`                         :math:`-1/2`                      :math:`0`
:math:`\mathrm{Y}`       :math:`1/2`                       :math:`0`                         :math:`0`
:math:`\mathrm{Z}`       :math:`-1/2`                      :math:`0`                         :math:`1/2`
=======================  ================================  ================================  ================================

Variations
==========

There are four variations of triclinic lattice.

TRI\ :sub:`1a`
--------------

:math:`k_{\alpha} > 90^{\circ}, k_{\beta} > 90^{\circ}, k_{\gamma} > 90^{\circ}, k_{\gamma} = \min(k_{\alpha}, k_{\beta}, k_{\gamma})`

TRI\ :sub:`2a`
--------------

:math:`k_{\alpha} > 90^{\circ}, k_{\beta} > 90^{\circ}, k_{\gamma} = 90^{\circ}`

TRI\ :sub:`1b`
--------------

:math:`k_{\alpha} < 90^{\circ}, k_{\beta} < 90^{\circ}, k_{\gamma} < 90^{\circ}, k_{\gamma} = \max(k_{\alpha}, k_{\beta}, k_{\gamma})`

TRI\ :sub:`2b`
--------------

:math:`k_{\alpha} < 90^{\circ}, k_{\beta} < 90^{\circ}, k_{\gamma} = 90^{\circ}`

In definition of the examples we cheated and defined them through reciprocal lattice parameters.

Examples
========

TRI\ :sub:`1a`
--------------

Brillouin zone and default kpath
--------------------------------
.. literalinclude:: tri1a_brillouin.py
    :language: py

.. raw:: html
    :file: tri1a_brillouin.html

Primitive and conventional cell
-------------------------------
.. literalinclude:: tri1a_real.py
    :language: py

.. raw:: html
    :file: tri1a_real.html

Wigner-Seitz cell
-----------------
.. literalinclude:: tri1a_wigner-seitz.py
    :language: py

.. raw:: html
    :file: tri1a_wigner-seitz.html

TRI\ :sub:`2a`
--------------

Brillouin zone and default kpath
--------------------------------
.. literalinclude:: tri2a_brillouin.py
    :language: py

.. raw:: html
    :file: tri2a_brillouin.html

Primitive and conventional cell
-------------------------------
.. literalinclude:: tri2a_real.py
    :language: py

.. raw:: html
    :file: tri2a_real.html

Wigner-Seitz cell
-----------------
.. literalinclude:: tri2a_wigner-seitz.py
    :language: py

.. raw:: html
    :file: tri2a_wigner-seitz.html

TRI\ :sub:`1b`
--------------

Brillouin zone and default kpath
--------------------------------
.. literalinclude:: tri1b_brillouin.py
    :language: py

.. raw:: html
    :file: tri1b_brillouin.html

Primitive and conventional cell
-------------------------------
.. literalinclude:: tri1b_real.py
    :language: py

.. raw:: html
    :file: tri1b_real.html

Wigner-Seitz cell
-----------------
.. literalinclude:: tri1b_wigner-seitz.py
    :language: py

.. raw:: html
    :file: tri1b_wigner-seitz.html

TRI\ :sub:`2b`
--------------

Brillouin zone and default kpath
--------------------------------
.. literalinclude:: tri2b_brillouin.py
    :language: py

.. raw:: html
    :file: tri2b_brillouin.html

Primitive and conventional cell
-------------------------------
.. literalinclude:: tri2b_real.py
    :language: py

.. raw:: html
    :file: tri2b_real.html

Wigner-Seitz cell
-----------------
.. literalinclude:: tri2b_wigner-seitz.py
    :language: py

.. raw:: html
    :file: tri2b_wigner-seitz.html




Cell standardization
====================

For the triclinic cell the standardization is performed on the reciprocal
primitive cell.

One of the four conditions have to be met:

* :math:`k_{\gamma} = 90^{\circ}` and other two angles are :math:`> 90^{\circ}`.

* :math:`k_{\gamma} = 90^{\circ}` and other two angles are :math:`< 90^{\circ}`.

* All reciprocal cell angles (:math:`k_{\alpha}`, :math:`k_{\beta}`, :math:`k_{\gamma}`) are :math:`> 90^{\circ}` and :math:`k_{\gamma} = \min(k_{\alpha}, k_{\beta}, k_{\gamma})`.

* All reciprocal cell angles (:math:`k_{\alpha}`, :math:`k_{\beta}`, :math:`k_{\gamma}`) are :math:`< 90^{\circ}` and :math:`k_{\gamma} = \max(k_{\alpha}, k_{\beta}, k_{\gamma})`.


First the reciprocal cell :math:`\boldsymbol{B}` is computed from the given primitive cell
:math:`\boldsymbol{A}`. Then the standardization matrix *for the reciprocal cell*
:math"`\boldsymbol{S}_1^{r}` is constructed in two steps

Step 1
------

In this step we ensure either of the two conditions: all angles are :math:`\le 90^{\circ}`
or all angles are :math:`\ge 90^{\circ}`.

* If :math:`k_{\alpha} \ge \frac{\pi}{2}` and :math:`k_{\beta} \ge \frac{\pi}{2}` and
  :math:`k_{\gamma} \ge \frac{\pi}{2}` or :math:`k_{\alpha} \le \frac{\pi}{2}` and
  :math:`k_{\beta} \le \frac{\pi}{2}` and :math:`k_{\gamma} \le \frac{\pi}{2}` then

  .. math::

    (\boldsymbol{b}_1^{(1)}, \boldsymbol{b}_2^{(1)}, \boldsymbol{b}_3^{(1)})
    =
    (\boldsymbol{b}_1, \boldsymbol{b}_2, \boldsymbol{b}_3)

  and

  .. math::

    \boldsymbol{S}_1^{r}
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}

* If :math:`k_{\alpha} \ge \frac{\pi}{2}` and :math:`k_{\beta} \ge \frac{\pi}{2}` and
  :math:`k_{\gamma} \le \frac{\pi}{2}` or :math:`k_{\alpha} \le \frac{\pi}{2}` and
  :math:`k_{\beta} \le \frac{\pi}{2}` and :math:`k_{\gamma} \ge \frac{\pi}{2}` then

  .. math::

    (\boldsymbol{b}_1^{(1)}, \boldsymbol{b}_2^{(1)}, \boldsymbol{b}_3^{(1)})
    =
    (-\boldsymbol{b}_1, -\boldsymbol{b}_2, \boldsymbol{b}_3)

  and

  .. math::

    \boldsymbol{S}_1
    =
    \begin{pmatrix}
      -1 & 0 & 0 \\
      0 & -1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}

* If :math:`k_{\alpha} \ge \frac{\pi}{2}` and :math:`k_{\beta} \le \frac{\pi}{2}` and
  :math:`k_{\gamma} \ge \frac{\pi}{2}` or :math:`k_{\alpha} \le \frac{\pi}{2}` and
  :math:`k_{\beta} \ge \frac{\pi}{2}` and :math:`k_{\gamma} \le \frac{\pi}{2}` then

  .. math::

    (\boldsymbol{b}_1^{(1)}, \boldsymbol{b}_2^{(1)}, \boldsymbol{b}_3^{(1)})
    =
    (-\boldsymbol{b}_1, \boldsymbol{b}_2, -\boldsymbol{b}_3)

  and

  .. math::

    \boldsymbol{S}_1
    =
    \begin{pmatrix}
      -1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & -1
    \end{pmatrix}

* If :math:`k_{\alpha} \le \frac{\pi}{2}` and :math:`k_{\beta} \ge \frac{\pi}{2}` and
  :math:`k_{\gamma} \ge \frac{\pi}{2}` or :math:`k_{\alpha} \ge \frac{\pi}{2}` and
  :math:`k_{\beta} \le \frac{\pi}{2}` and :math:`k_{\gamma} \le \frac{\pi}{2}` then

  .. math::

    (\boldsymbol{b}_1^{(1)}, \boldsymbol{b}_2^{(1)}, \boldsymbol{b}_3^{(1)})
    =
    (\boldsymbol{b}_1, -\boldsymbol{b}_2, -\boldsymbol{b}_3)

  and

  .. math::

    \boldsymbol{S}_1
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & -1 & 0 \\
      0 & 0 & -1
    \end{pmatrix}

Step 2
------

At this step we ensure that :math:`k_{\gamma}` is an appropriate extremum.

* If :math:`k_{\gamma} = min(k_{\alpha}, k_{\beta}, k_{\gamma})` and
  :math:`k_{\gamma} \ge \frac{\pi}{2}` or
  :math:`k_{\gamma} = max(k_{\alpha}, k_{\beta}, k_{\gamma})` and
  :math:`k_{\gamma} \le \frac{\pi}{2}` then

  .. math::

    (\boldsymbol{b}_1^s, \boldsymbol{b}_2^s, \boldsymbol{b}_3^s)
    =
    (\boldsymbol{b}_1^{(1)}, \boldsymbol{b}_2^{(1)}, \boldsymbol{b}_3^{(1)})

  and

  .. math::

    \boldsymbol{S}_2
    =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}

* If :math:`k_{\beta} = min(k_{\alpha}, k_{\beta}, k_{\gamma})` and
  :math:`k_{\beta} \ge \frac{\pi}{2}` or
  :math:`k_{\beta} = max(k_{\alpha}, k_{\beta}, k_{\gamma})` and
  :math:`k_{\beta} \le \frac{\pi}{2}` then

  .. math::

    (\boldsymbol{b}_1^s, \boldsymbol{b}_2^s, \boldsymbol{b}_3^s)
    =
    (\boldsymbol{b}_3^{(1)}, \boldsymbol{b}_1^{(1)}, \boldsymbol{b}_2^{(1)})

  and

  .. math::

    \boldsymbol{S}_2
    =
    \begin{pmatrix}
      0 & 1 & 0 \\
      0 & 0 & 1 \\
      1 & 0 & 0
    \end{pmatrix}

* If :math:`k_{\alpha} = min(k_{\alpha}, k_{\beta}, k_{\gamma})` and
  :math:`k_{\alpha} \ge \frac{\pi}{2}` or
  :math:`k_{\alpha} = max(k_{\alpha}, k_{\beta}, k_{\gamma})` and
  :math:`k_{\alpha} \le \frac{\pi}{2}` then

  .. math::

    (\boldsymbol{b}_1^s, \boldsymbol{b}_2^s, \boldsymbol{b}_3^s)
    =
    (\boldsymbol{b}_2^{(1)}, \boldsymbol{b}_3^{(1)}, \boldsymbol{b}_1^{(1)})

  and

  .. math::

    \boldsymbol{S}_2
    =
    \begin{pmatrix}
      0 & 0 & 1 \\
      1 & 0 & 0 \\
      0 & 1 & 0
    \end{pmatrix}

Finally
-------

.. math::

  \boldsymbol{S}
  =
  ((\boldsymbol{S}_1\boldsymbol{S}_2)^T)^{-1}
  \qquad
  \boldsymbol{S}^{-1}
  =
  (\boldsymbol{S}_1\boldsymbol{S}_2)^T
