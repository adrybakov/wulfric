.. _module-guide:

************
Module guide
************

Module guide is directed at the users, who wants to use the package as python library.
The main objective of the module guide is to
familiarize you with the package and provide examples of usage.


Data structure and import
=========================

wulfric is a collection of submodules, which combine the classes and functions
with the same topic. For the full reference of the submodules, please refer to the
:ref:`api`.

All public methods of each submodule are exposed to the main entry
point (``wulfric``):

.. doctest::

    >>> from wulfric import Crystal, print_2d_array, Cell, SpinHamiltonian

Explicit imports are supported as well:

.. doctest::

    >>> from wulfric.crystal import Crystal, Cell
    >>> from wulfric.decorate import print_2d_array
    >>> from wulfric.spinham import SpinHamiltonian

As well as the exact imports:

.. doctest::

        >>> from wulfric.crystal.crystal import Crystal
        >>> from wulfric.crystal import cell as Cell
        >>> from wulfric.decorate.array import print_2d_array
        >>> from wulfric.spinham.hamiltonian import SpinHamiltonian

The first method is recommended for the user, as it is the most convenient
and provides the most intuitive way of using the package.

The third method is useful for the
advanced users, who wants to :ref:`contribute <contribute>` to the package.

In the examples of this guide, the first import method is used, unless stated otherwise.

Relation between classes
------------------------
Classes in wulfric illustrate a physical or mathematical
concept (i.e. :py:class:`.MagnonDispersion`, :py:class:`.Kpoints`, ...)
or object (i.e. :py:class:`.Atom`, :py:class:`.Lattice`, :py:class:`.Crystal`, ...).
The relations between the classes could be roughly illustrated by the following diagram:

.. figure:: ../../img/class-relation.png
    :align: center
    :target: ../../_images/class-relation.png

Submodules
==========

For the detailed guide on each submodule please refer to the corresponding page:

.. toctree::
    :maxdepth: 1

    crystal/index
    io/index
    geometry
    numerical
    decorate
