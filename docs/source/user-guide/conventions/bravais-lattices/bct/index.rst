.. _guide_bct:

*****************************
Body-centred tetragonal (BCT)
*****************************

**Pearson symbol**: tI

**Constructor**:  :py:func:`.BCT`

It is defined by two parameters: :math:`a` and :math:`c` with
conventional cell:

.. math::

    \begin{matrix}
    \boldsymbol{a}_1^c &=& (a, &0, &0)\\
    \boldsymbol{a}_2^c &=& (0, &a, &0)\\
    \boldsymbol{a}_3^c &=& (0, &0, &c)
    \end{matrix}

And primitive cell:

.. math::

    \begin{matrix}
    \boldsymbol{a}_1 &=& (-a/2, &a/2, &c/2)\\
    \boldsymbol{a}_2 &=& (a/2, &-a/2, &c/2)\\
    \boldsymbol{a}_3 &=& (a/2, &a/2, &-c/2)
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

Order of parameters: :math:`a \ne c`

K-path
======

BCT\ :sub:`1`
-------------

:math:`\mathrm{\Gamma-X-M-\Gamma-Z-P-N-Z_1-M\vert X-P}`

.. math::

    \eta = \dfrac{1 + c^2/a^2}{4}

=======================  ==============================  ==============================  ==============================
Point                    :math:`\times\boldsymbol{b}_1`  :math:`\times\boldsymbol{b}_2`  :math:`\times\boldsymbol{b}_3`
=======================  ==============================  ==============================  ==============================
:math:`\mathrm{\Gamma}`  :math:`0`                       :math:`0`                       :math:`0`
:math:`\mathrm{M}`       :math:`-1/2`                    :math:`1/2`                     :math:`1/2`
:math:`\mathrm{N}`       :math:`0`                       :math:`1/2`                     :math:`0`
:math:`\mathrm{P}`       :math:`1/4`                     :math:`1/4`                     :math:`1/4`
:math:`\mathrm{X}`       :math:`0`                       :math:`0`                       :math:`1/2`
:math:`\mathrm{Z}`       :math:`\eta`                    :math:`\eta`                    :math:`-\eta`
:math:`\mathrm{Z}_1`     :math:`-\eta`                   :math:`1-\eta`                  :math:`\eta`
=======================  ==============================  ==============================  ==============================

BCT\ :sub:`2`
-------------

:math:`\mathrm{\Gamma-X-Y-\Sigma-\Gamma-Z-\Sigma_1-N-P-Y_1-Z\vert X-P}`

.. math::

    \begin{matrix}
    \eta = \dfrac{1 + a^2/c^2}{4} &
    \zeta = \dfrac{a^2}{2c^2}
    \end{matrix}

=========================  ==============================  ==============================  ==============================
Point                      :math:`\times\boldsymbol{b}_1`  :math:`\times\boldsymbol{b}_2`  :math:`\times\boldsymbol{b}_3`
=========================  ==============================  ==============================  ==============================
:math:`\mathrm{\Gamma}`    :math:`0`                       :math:`0`                       :math:`0`
:math:`\mathrm{N}`         :math:`0`                       :math:`1/2`                     :math:`0`
:math:`\mathrm{P}`         :math:`1/4`                     :math:`1/4`                     :math:`1/4`
:math:`\mathrm{\Sigma}`    :math:`-\eta`                   :math:`\eta`                    :math:`\eta`
:math:`\mathrm{\Sigma_1}`  :math:`\eta`                    :math:`1-\eta`                  :math:`-\eta`
:math:`\mathrm{X}`         :math:`0`                       :math:`0`                       :math:`1/2`
:math:`\mathrm{Y}`         :math:`-\zeta`                  :math:`\zeta`                   :math:`1/2`
:math:`\mathrm{Y}_1`       :math:`1/2`                     :math:`1/2`                     :math:`-\zeta`
:math:`\mathrm{Z}`         :math:`1/2`                     :math:`1/2`                     :math:`-1/2`
=========================  ==============================  ==============================  ==============================


Variations
==========

There are two variations of body-centered tetragonal lattice.

BCT\ :sub:`1`
-------------

:math:`c < a`.

Predefined example: ``bct1`` with :math:`a = 1.5\pi` and :math:`c = \pi`.

BCT\ :sub:`2`
-------------

:math:`c > a`.

Predefined example: ``bct2`` with :math:`a = \pi` and :math:`c = 1.5\pi`.


Examples
========

BCT\ :sub:`1`
-------------

Brillouin zone and default kpath
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: bct1_brillouin.py
    :language: py

.. raw:: html
    :file: bct1_brillouin.html

Primitive and conventional cell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: bct1_real.py
    :language: py

.. raw:: html
    :file: bct1_real.html

Wigner-Seitz cell
^^^^^^^^^^^^^^^^^
.. literalinclude:: bct1_wigner-seitz.py
    :language: py

.. raw:: html
    :file: bct1_wigner-seitz.html

BCT\ :sub:`2`
-------------


Brillouin zone and default kpath
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: bct2_brillouin.py
    :language: py

.. raw:: html
    :file: bct2_brillouin.html

Primitive and conventional cell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: bct2_real.py
    :language: py

.. raw:: html
    :file: bct2_real.html

Wigner-Seitz cell
^^^^^^^^^^^^^^^^^
.. literalinclude:: bct2_wigner-seitz.py
    :language: py

.. raw:: html
    :file: bct2_wigner-seitz.html


Cell standardization
====================

Condition :math:`a \ne c` result in the condition :math:`\alpha = \beta \ne \gamma` for
the primitive cell in a standard form, in practice this condition simplifies to
:math:`\boldsymbol{a}_1^s\cdot\boldsymbol{a}_2^s \ne \boldsymbol{a}_1^s\cdot\boldsymbol{a}_3^s`
and
:math:`\boldsymbol{a}_1^s\cdot\boldsymbol{a}_3^s = \boldsymbol{a}_2^s\cdot\boldsymbol{a}_3^s`
for the primitive cell in a standard form.
We use angles of the primitive cell for standardization.

* If
  :math:`\alpha = \beta \ne \gamma` (i.e.
  :math:`\boldsymbol{a}_2\cdot\boldsymbol{a}_3 = \boldsymbol{a}_1\cdot\boldsymbol{a}_3 \ne \boldsymbol{a}_1\cdot\boldsymbol{a}_2`),
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

* If
  :math:`\beta = \gamma \ne \alpha` (i.e.
  :math:`\boldsymbol{a}_1\cdot\boldsymbol{a}_3 = \boldsymbol{a}_1\cdot\boldsymbol{a}_2 \ne \boldsymbol{a}_2\cdot\boldsymbol{a}_3`),
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

* If
  :math:`\alpha = \gamma \ne \beta` (i.e.
  :math:`\boldsymbol{a}_2\cdot\boldsymbol{a}_3 = \boldsymbol{a}_1\cdot\boldsymbol{a}_2 \ne \boldsymbol{a}_1\cdot\boldsymbol{a}_3`),
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

Edge cases
==========

If :math:`a = c` then the lattice is :ref:`guide_bcc`.
