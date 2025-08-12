.. _user-guide_usage_other:

***************
Other functions
***************

On this page we describe formally unrelated functions and modules of wulfric that were not
mentioned in the previous pages. We do not describe all of them. To see full list of
wulfric capabilities see :ref:`api`.

In the examples of this page we assume that wulfric is imported as

.. doctest::

  >>> import wulfric as wulf


Comparing of numbers
====================

Due to the limitations of the float point arithmetics or expected inaccuracy of the input
data two numbers might be considered equal even if they are not exactly equal. For example
``1.0000000001`` and ``1.0000000002`` are equal with the accuracy ``1e-9``, but different with
the accuracy of ``1e-11``. Same logic can be applied to other comparison operators. We
enjoyed the formal definition from [1]_ and implemented it as a standalone function in
wulfric

.. doctest::

    >>> wulf.compare_numerically(1.0000000001, "==", 1.0000000002, eps=1e-9)
    True
    >>> wulf.compare_numerically(1.0000000001, "==", 1.0000000002, eps=1e-11)
    False
    >>> wulf.compare_numerically(1.02, "<", 1.03, eps=0.001)
    True
    >>> wulf.compare_numerically(1.02, "<", 1.03, eps=0.1)
    False
    >>> wulf.compare_numerically(1.02, "<=", 1.03, eps=0.1)
    True

This function return boolean value and support python's comparison operators.
See :py:func:`.compare_numerically` for details.


Parallelepiped
==============
Not any set of six numbers might be used to form a parallelepiped. Wulfric implements a
function to check if the set of parameters is correct

.. doctest::

    >>> a = 1
    >>> b = 1
    >>> c = 1
    >>> alpha = 90
    >>> beta = 90
    >>> gamma = 90
    >>> wulf.geometry.parallelepiped_check(a, b, c, alpha, beta, gamma)
    True
    >>> wulf.geometry.parallelepiped_check(a, b, c, alpha, beta, 181)
    False


Volume and angle
================

It is often required to compute angle between two vectors or a volume of the cell.
Wulfric implements two functions just for that.

To compute an angle between two vectors use

.. doctest::

    >>> a = [1, 0, 0]
    >>> b = [0, 1, 0]
    >>> # In degrees by default
    >>> wulf.geometry.get_angle(a, b)
    90.0
    >>> # In radians
    >>> round(wulf.geometry.get_angle(a, b, radians=True), 4)
    1.5708
    >>> # For the zero vector the angle is not defined
    >>> wulf.geometry.get_angle(a, [0, 0, 0])
    Traceback (most recent call last):
    ...
    ValueError: Angle is ill defined (zero vector).

For the volume wulfric accepts three types of inputs:

* Cell

  :math:`3\times3` array, rows are the cell vectors, columns are the :math:`xyz` coordinates.

  .. doctest::

      >>> cell = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
      >>> wulf.geometry.get_volume(cell)
      1.0

* Three vectors

  .. doctest::

      >>> a = [1, 0, 0]
      >>> b = [0, 1, 0]
      >>> c = [0, 0, 1]
      >>> wulf.geometry.get_volume(a, b, c)
      1.0

* Six cell parameters

  .. doctest::

      >>> a = 1
      >>> b = 1
      >>> c = 1
      >>> alpha = 90
      >>> beta = 90
      >>> gamma = 90
      >>> wulf.geometry.get_volume(a, b, c, alpha, beta, gamma)
      1.0

Spherical coordinates
=====================

.. doctest::

    >>> import wulfric as wulf
    >>> wulf.geometry.get_spherical([1, 0, 0])
    (1.0, 90.0, 0.0)
    >>> wulf.geometry.get_spherical([-1, 0, 0])
    (1.0, 90.0, 180.0)
    >>> wulf.geometry.get_spherical([0, 1, 0])
    (1.0, 90.0, 90.0)
    >>> wulf.geometry.get_spherical([0, -1, 0])
    (1.0, 90.0, 270.0)
    >>> wulf.geometry.get_spherical([0, 0, 1])
    (1.0, 0.0, 0.0)
    >>> wulf.geometry.get_spherical([0, 0, -1])
    (1.0, 180.0, 180.0)
    >>> wulf.geometry.get_spherical([1, 0, 0], polar_axis = [1, 0, 0])
    (1.0, 0.0, 0.0)


References
==========
.. [1] Grosse-Kunstleve, R.W., Sauter, N.K. and Adams, P.D., 2004.
    Numerically stable algorithms for the computation of reduced unit cells.
    Acta Crystallographica Section A: Foundations of Crystallography,
    60(1), pp.1-6.
