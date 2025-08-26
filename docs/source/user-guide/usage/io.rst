.. _user-guide_usage_io:


************
Input-output
************

For the full technical reference see :ref:`api_io`.

In the examples of this page we assume that wulfric is imported as

.. doctest::

  >>> import wulfric

VASP
====

Wulfric can read and write VASP |POSCAR|_ files.

Reading
-------

.. doctest::

  >>> # Load a POSCAR file
  >>> cell, atoms, comment = wulfric.io.load_poscar('POSCAR') # doctest: +SKIP

Writing
-------

.. doctest::

  >>> # Dump a POSCAR file
  >>> wulfric.io.dump_poscar(cell, atoms, 'POSCAR') # doctest: +SKIP
  >>> # If you want to write a comment as well:
  >>> wulfric.io.dump_poscar(cell, atoms, 'POSCAR', comment='This is a comment') # doctest: +SKIP
  >>> # You can control the amount of decimals in the output:
  >>> wulfric.io.dump_poscar(cell, atoms, 'POSCAR', decimals=6) # doctest: +SKIP
  >>> # You can switch the mode of coordinates between 'Cartesian' and 'Direct' (default):
  >>> wulfric.io.dump_poscar(cell, atoms, 'POSCAR', mode="Cartesian") # doctest: +SKIP
