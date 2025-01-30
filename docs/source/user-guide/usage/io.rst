.. _user-guide_usage_io:


************
Input-output
************

For the full technical reference see :ref:`api_io`.

In the examples of this page we assume that wulfric is imported as

.. doctest::

  >>> import wulfric as wulf

VASP
====

Wulfric can read and write VASP |POSCAR|_ files.

Reading
-------

.. doctest::

  >>> # Load a POSCAR file
  >>> cell, atoms = wulf.io.load_poscar('POSCAR') # doctest: +SKIP
  >>> # It can return the comment from the file as well:
  >>> cell, atoms, comment = wulf.io.load_poscar('POSCAR', return_comment=True) # doctest: +SKIP

Writing
-------

.. doctest::

  >>> # Dump a POSCAR file
  >>> wulf.io.dump_poscar(cell, atoms, 'POSCAR') # doctest: +SKIP
  >>> # If you want to write a comment as well:
  >>> wulf.io.dump_poscar(cell, atoms, 'POSCAR', comment='This is a comment') # doctest: +SKIP
  >>> # You can control the amount of decimals in the output:
  >>> wulf.io.dump_poscar(cell, atoms, 'POSCAR', decimals=6) # doctest: +SKIP
  >>> # You can switch the mode of coordinates between 'Cartesian' and 'Direct' (default):
  >>> wulf.io.dump_poscar(cell, atoms, 'POSCAR', mode="Cartesian") # doctest: +SKIP
