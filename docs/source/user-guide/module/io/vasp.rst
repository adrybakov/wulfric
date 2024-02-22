.. _guide_io_vasp:

.. currentmodule:: wulfric

**************
VASP interface
**************

For the full technical reference see :ref:`api_io`.

Wulfric can read and write VASP |POSCAR|_ files.

Import
======

.. doctest::

  >>> # Explicit import
  >>> from wulfric.io.vasp import load_poscar, dump_poscar
  >>> # Recommended import
  >>> from wulfric import load_poscar, dump_poscar


Reading
=======

.. doctest::

  >>> # Load a POSCAR file
  >>> crystal = load_poscar('POSCAR') # doctest: +SKIP
  >>> # It can return cell and a list of Atom objects instead of a Crystal instance
  >>> cell, atoms = load_poscar('POSCAR', return_cell=False) # doctest: +SKIP
  >>> # It can return the comment from the file as well:
  >>> crystal, comment = load_poscar('POSCAR', return_comment=True) # doctest: +SKIP
  >>> # Or
  >>> cell, atoms, comment = load_poscar('POSCAR', return_cell=False, return_comment=True) # doctest: +SKIP

Writing
=======

.. doctest::

  >>> # Dump a POSCAR file
  >>> dump_poscar(crystal, 'POSCAR') # doctest: +SKIP
  >>> # If you want to write a comment as well:
  >>> dump_poscar(crystal, 'POSCAR', comment='This is a comment') # doctest: +SKIP
  >>> # You can control the amount of decimals in the output:
  >>> dump_poscar(crystal, 'POSCAR', decimals=6) # doctest: +SKIP
  >>> # You can switch the mode of coordinates between 'Cartesian' and 'Direct' (default):
  >>> dump_poscar(crystal, 'POSCAR', mode="Cartesian") # doctest: +SKIP
