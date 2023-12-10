.. _user-guide_about:

****************
What is WULFRIC?
****************

WULFRIC is a python package for the structural part of the condense matter codes.
It combines the concept of the :ref:`Lattice <user-guide_module_lattice>`,
:ref:`Atom <user-guide_module_atom>` and :ref:`Crystal <user-guide_module_crystal>`
and provides a simple skeleton for other codes to built on.

It provides the automatic choice of the :ref:`Kpoints <user-guide_module_kpoints>`
and K-path for all :ref:`Bravais lattice types <library_bravais-lattices>`.

Initially it was a part of the `RAD-tools <https://rad-tools.org>`_ package,
but later separated from it to provide the reusable part for other projects.

.. note::
  The terminal output is colored, however we respect `NO_COLOR <https://no-color.org/>`_.
