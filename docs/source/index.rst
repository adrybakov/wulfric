*******
Wulfric
*******

.. toctree::
    :maxdepth: 1
    :hidden:

    user-guide/start/installation
    User Guide <user-guide/index>
    api/index
    release-notes/index
    contribute/index
    cite
    support

:Release: |version|
:Date: |release_date|

**Useful links**:
:ref:`Installation <user-guide_start_installation>` |
`Issue Tracker <https://github.com/adrybakov/wulfric/issues>`_ |
:ref:`Cite us <wulfric_cite>` |
:ref:`support`

****************
What is wulfric?
****************

Wulfric is a python package for the description and symmetries of crystal structures.
It uses a simple concepts of ``cell`` and ``atoms`` and provides a simple skeleton for
other codes to built on. (see :ref:`user-guide_usage_key-concepts`)

The functional of wulfric includes (but not limited to):

* Calculation of Bravais lattice type and variation.

* Automatic choice of the :ref:`Kpoints <user-guide_usage_kpoints>`
  and K-path for all :ref:`Bravais lattice types <user-guide_conventions_bravais-lattices>`.

* Set of useful functions for :ref:`user-guide_usage_cell`, :ref:`user-guide_usage_crystal`.

* Standalone :py:func:`.lepage` and :py:func:`.niggli` algorithms.


.. grid:: 2

    .. grid-item-card::
        :img-top: _static/index-images/quickstart.svg

        Getting Started
        ^^^^^^^^^^^^^^^

        Check out the Quickstart Guide.

        +++

        .. button-ref:: user-guide/start/quickstart
            :expand:
            :color: primary
            :click-parent:

            To the quickstart guide

    .. grid-item-card::
        :img-top: _static/index-images/user-guide.svg

        User Guide
        ^^^^^^^^^^

        User guide describes two main ways of using wulfric.

        +++

        .. button-ref:: user-guide/index
            :expand:
            :color: primary
            :click-parent:

            To the user guide

    .. grid-item-card::
        :img-top: _static/index-images/api.svg

        API Reference
        ^^^^^^^^^^^^^

        Api Reference guide describes all classes and method of the package,
        how they work and which parameters they support.
        +++

        .. button-ref:: api/index
            :expand:
            :color: primary
            :click-parent:

            To the API reference

    .. grid-item-card::
        :img-top: _static/index-images/contributor.svg

        Contributor's Guide
        ^^^^^^^^^^^^^^^^^^^

        Every kind of contribution is welcomed!

        +++

        .. button-ref:: contribute/index
            :expand:
            :color: primary
            :click-parent:

            To the contributor's guide

.. note::
  The terminal output is colored by default. However, we respect `NO_COLOR <https://no-color.org/>`_.
