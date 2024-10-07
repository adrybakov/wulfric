.. _guide_orci:

********************************
Body-centred orthorhombic (ORCI)
********************************

**Pearson symbol**: oI

**Constructor**:  :py:func:`.ORCI`

It is defined by three parameter: :math:`a`, :math:`b` and :math:`c`
with conventional cell:

.. math::

    \begin{matrix}
    \boldsymbol{a}_1^c &=& (a, &0, &0)\\
    \boldsymbol{a}_2^c &=& (0, &b, &0)\\
    \boldsymbol{a}_3^c &=& (0, &0, &c)
    \end{matrix}

And primitive cell:

.. math::

    \begin{matrix}
    \boldsymbol{a}_1 &=& (-a/2, &b/2, &c/2)\\
    \boldsymbol{a}_2 &=& (a/2, &-b/2, &c/2)\\
    \boldsymbol{a}_3 &=& (a/2, &b/2, &-c/2)
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

Order of parameters: :math:`a < b < c`

K-path
======

:math:`\mathrm{\Gamma-X-L-T-W-R-X_1-Z-\Gamma-Y-S-W\vert L_1-Y\vert Y_1-Z}`

.. math::

    \begin{matrix}
    \zeta = \dfrac{1 + a^2/c^2}{4} &
    \eta = \dfrac{1 + b^2/c^2}{4} &
    \delta = \dfrac{b^2 - a^2}{4c^2} &
    \mu = \dfrac{a^2 + b^2}{4c^2}
    \end{matrix}

=========================  ==============================  ==============================  ==============================
Point                      :math:`\times\boldsymbol{b}_1`  :math:`\times\boldsymbol{b}_2`  :math:`\times\boldsymbol{b}_3`
=========================  ==============================  ==============================  ==============================
:math:`\mathrm{\Gamma}`    :math:`0`                       :math:`0`                       :math:`0`
:math:`\mathrm{L}`         :math:`-\mu`                    :math:`\mu`                     :math:`1/2 - \delta`
:math:`\mathrm{L_1}`       :math:`\mu`                     :math:`-\mu`                    :math:`1/2 + \delta`
:math:`\mathrm{L_2}`       :math:`1/2-\delta`              :math:`1/2+\delta`              :math:`-\mu`
:math:`\mathrm{R}`         :math:`0`                       :math:`1/2`                     :math:`0`
:math:`\mathrm{S}`         :math:`1/2`                     :math:`0`                       :math:`0`
:math:`\mathrm{T}`         :math:`0`                       :math:`0`                       :math:`1/2`
:math:`\mathrm{W}`         :math:`1/4`                     :math:`1/4`                     :math:`1/4`
:math:`\mathrm{X}`         :math:`-\zeta`                  :math:`\zeta`                   :math:`\zeta`
:math:`\mathrm{X_1}`       :math:`\zeta`                   :math:`1-\zeta`                 :math:`-\zeta`
:math:`\mathrm{Y}`         :math:`\eta`                    :math:`-\eta`                   :math:`\eta`
:math:`\mathrm{Y_1}`       :math:`1-\eta`                  :math:`\eta`                    :math:`-\eta`
:math:`\mathrm{Z}`         :math:`1/2`                     :math:`1/2`                     :math:`-1/2`
=========================  ==============================  ==============================  ==============================


Variations
==========

There are no variations for body-centered orthorombic.
One example is predefined: ``orci`` with
:math:`a = \pi`, :math:`b  = 1.3\pi` and :math:`c = 1.7\pi`.

Examples
========

Brillouin zone and default kpath
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: orci_brillouin.py
    :language: py

.. raw:: html
    :file: orci_brillouin.html

Primitive and conventional cell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: orci_real.py
    :language: py

.. raw:: html
    :file: orci_real.html

Wigner-Seitz cell
^^^^^^^^^^^^^^^^^
.. literalinclude:: orci_wigner-seitz.py
    :language: py

.. raw:: html
    :file: orci_wigner-seitz.html


Cell standardization
====================

Condition :math:`a < b < b` result in the condition :math:`\gamma > \beta > \alpha` for
the primitive cell in a standard form, in practice this condition simplifies to
:math:`\boldsymbol{a}_1^s\cdot\boldsymbol{a}_2^s > \boldsymbol{a}_1^s\cdot\boldsymbol{a}_3^s > \boldsymbol{a}_2^s\cdot\boldsymbol{a}_3^s`
for the primitive cell in a standard form. Therefore, for the given primitive cell the
algorithm is:

FIXME: potentially wrong second step!


First we order :math:`\alpha` and :math:`\beta`:

* If :math:`\alpha > \beta` (i.e. :math:`\boldsymbol{a}_2\cdot\boldsymbol{a}_3 > \boldsymbol{a}_1\cdot\boldsymbol{a}_3`), then

  .. math::

    (\boldsymbol{\tilde{a}}_1, \boldsymbol{\tilde{a}}_2, \boldsymbol{\tilde{a}}_3)
    =
    (-\boldsymbol{a}_1, -\boldsymbol{a}_2, \boldsymbol{a}_3)

  and

  .. math::

    \boldsymbol{\tilde{S}} =
    \begin{pmatrix}
      -1 & 0 & 0 \\
      0 & -1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}

* Else

  .. math::

    (\boldsymbol{\tilde{a}}_1, \boldsymbol{\tilde{a}}_2, \boldsymbol{\tilde{a}}_3)
    =
    (\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)

  and

  .. math::

    \boldsymbol{\tilde{S}} =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & 1 & 0 \\
      0 & 0 & 1
    \end{pmatrix}

Then we place :math:`\gamma` in the correct place:

* If :math:`\gamma < \alpha` (i.e. :math:`\boldsymbol{\tilde{a}}_1\cdot\boldsymbol{\tilde{a}}_2 < \boldsymbol{\tilde{a}}_2\cdot\boldsymbol{\tilde{a}}_3`), then

  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s) =
    (\boldsymbol{\tilde{a}}_3, \boldsymbol{\tilde{a}}_1, \boldsymbol{\tilde{a}}_2)

  and

  .. math::

    \boldsymbol{S} =
    \begin{pmatrix}
      0 & 0 & 1 \\
      1 & 0 & 0 \\
      0 & 1 & 0
    \end{pmatrix}
    \cdot
    \boldsymbol{\tilde{S}}

* If :math:`\alpha < \gamma < \beta` (i.e. :math:`\boldsymbol{\tilde{a}}_2\cdot\boldsymbol{\tilde{a}}_3 < \boldsymbol{\tilde{a}}_1\cdot\boldsymbol{\tilde{a}}_2 < \boldsymbol{\tilde{a}}_1\cdot\boldsymbol{\tilde{a}}_3`), then
  .. math::

    (\boldsymbol{a}_1^s, \boldsymbol{a}_2^s, \boldsymbol{a}_3^s) =
    (\boldsymbol{\tilde{a}}_1, -\boldsymbol{\tilde{a}}_2, -\boldsymbol{\tilde{a}}_3)

  and

  .. math::

    \boldsymbol{S} =
    \begin{pmatrix}
      1 & 0 & 0 \\
      0 & -1 & 0 \\
      0 & 0 & -1
    \end{pmatrix}
    \cdot
    \boldsymbol{\tilde{S}}

* Else

  .. math::

    \boldsymbol{S}
    =
    \boldsymbol{\tilde{S}}

.. note::

    The third lattice vector is multiplied by :math:`-1` in some cases to
    preserve the handedness of the cell.

Edge cases
==========
If :math:`a = b \ne c` or :math:`a = c \ne b` or :math:`b = c \ne a`,
then the lattice is :ref:`guide_bct`.

If :math:`a = b = c`, then the lattice is :ref:`guide_bcc`.
