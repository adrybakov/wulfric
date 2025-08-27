.. _user-guide_conventions_bravais-lattices:

****************
Bravais lattices
****************

.. currentmodule:: wulfric

For the full technical reference see :ref:`api_cell`

Bravais lattice notation and standardization follows Setyawan and Curtarolo [1]_.

For each Bravais lattice type wulfric can compute the standard form of the primitive:
:math:`\boldsymbol{A}^s` and the conventional :math:`\boldsymbol{A}^{cs}` cells as defined
in the reference paper [1]_.

The cell can be given to wulfric in any orientation. Standardization procedure does not
change the orientation of the lattice/crystal, but redefine the lattice vectors. For
instance, the ``cell`` and relative positions of ``atoms`` might change, but the
underlying lattice and positions of ``atoms`` in the real space are not modified. The
K-points are computed for the original (given) unit cell, using the transformation matrix
:math:`\boldsymbol{S}` from given to standardized cell.

In each individual page, relative positions of the high-symmetry k-points are written for
the *standardized primitive* cell in the *default* orientation. The actual relative
coordinates of the k-points that wulfric computes are specific to the ``cell`` that user
provides (original cell) and may differ from the ones written in those pages.

There is no need for the user to standardize the cell to have access to the k-points.
However, it is the user's responsibility to track whether the given cell is *primitive*.
The k-points will be computed even if the cell is not primitive and the Bravais lattice
type will be defined by *interpreting* the given cell as primitive.

.. note::
  The images are interactive.


Cubic lattice system
--------------------

.. toctree::
    :hidden:

    cub/index
    fcc/index
    bcc/index

=================  ==========  ===============  ================
Name               Examples    Parameters       Constructor
=================  ==========  ===============  ================
:ref:`guide_cub`   ``cub``     :math:`a`        :py:func:`.CUB`
:ref:`guide_fcc`   ``fcc``     :math:`a`        :py:func:`.FCC`
:ref:`guide_bcc`   ``bcc``     :math:`a`        :py:func:`.BCC`
=================  ==========  ===============  ================

Tetragonal lattice system
-------------------------

.. toctree::
    :hidden:

    tet/index
    bct/index

=================  ==========  ===============  ================
Name               Examples    Parameters       Constructor
=================  ==========  ===============  ================
:ref:`guide_tet`   ``tet``     :math:`a`,       :py:func:`.TET`
                               :math:`c`
:ref:`guide_bct`   ``bct``,    :math:`a`,       :py:func:`.BCT`
                   ``bct1``,   :math:`c`
                   ``bct2``
=================  ==========  ===============  ================

Orthorhombic lattice system
---------------------------

.. toctree::
    :hidden:

    orc/index
    orcf/index
    orci/index
    orcc/index

=================  ==========  ===============  ================
Name               Examples    Parameters       Constructor
=================  ==========  ===============  ================
:ref:`guide_orc`   ``orc``     :math:`a`,       :py:func:`.ORC`
                               :math:`b`,
                               :math:`c`
:ref:`guide_orcf`  ``orcf``,   :math:`a`,       :py:func:`.ORCF`
                   ``orcf1``,  :math:`b`,
                   ``orcf2``,  :math:`c`
                   ``orcf3``
:ref:`guide_orci`  ``orci``    :math:`a`,       :py:func:`.ORCI`
                               :math:`b`,
                               :math:`c`
:ref:`guide_orcc`  ``orcc``    :math:`a`,       :py:func:`.ORCC`
                               :math:`b`,
                               :math:`c`
=================  ==========  ===============  ================

Hexagonal lattice system
------------------------

.. toctree::
    :hidden:

    hex/index

=================  ==========  ===============  ================
Name               Examples    Parameters       Constructor
=================  ==========  ===============  ================
:ref:`guide_hex`   ``hex``     :math:`a`,       :py:func:`.HEX`
                               :math:`c`
=================  ==========  ===============  ================

Rhombohedral lattice system
---------------------------

.. toctree::
    :hidden:

    rhl/index

=================  ==========  ===============  ================
Name               Examples    Parameters       Constructor
=================  ==========  ===============  ================
:ref:`guide_rhl`   ``rhl``,    :math:`a`,       :py:func:`.RHL`
                   ``rhl1``,   :math:`c`
                   ``rhl2``
=================  ==========  ===============  ================

Monoclinic lattice system
-------------------------

.. toctree::
    :hidden:

    mcl/index
    mclc/index

=================  ==========  ===============  ================
Name               Examples    Parameters       Constructor
=================  ==========  ===============  ================
:ref:`guide_mcl`   ``mcl``     :math:`a`,       :py:func:`.MCL`
                               :math:`b`,
                               :math:`c`,
                               :math:`\alpha`
:ref:`guide_mclc`  ``mclc``,   :math:`a`,       :py:func:`.MCLC`
                   ``mclc1``,  :math:`b`,
                   ``mclc2``,  :math:`c`,
                   ``mclc3``,  :math:`\alpha`
                   ``mclc4``,
                   ``mclc5``
=================  ==========  ===============  ================

Triclinic lattice system
------------------------

Predefined examples: ``tri1a``, ``tri1b``, ``tri2a``, ``tri2b``.

.. toctree::
    :hidden:

    tri/index

=================  ==========  ===============  ================
Name               Examples    Parameters       Constructor
=================  ==========  ===============  ================
:ref:`guide_tri`   ``tri1a``,  :math:`a`,       :py:func:`.TRI`
                   ``tri1b``,  :math:`b`,
                   ``tri2a``,  :math:`c`,
                   ``tri2b``   :math:`\alpha`,
                               :math:`\beta`,
                               :math:`\gamma`
=================  ==========  ===============  ================

References
==========
.. [1] Setyawan, W. and Curtarolo, S., 2010.
    High-throughput electronic band structure calculations: Challenges and tools.
    Computational materials science, 49(2), pp. 299-312.
