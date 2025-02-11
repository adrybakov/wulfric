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

Relative vs absolute
====================

For the set of ``atoms`` and a reference ``cell`` it is an often task to transform from
relative to the absolute coordinates and vice versa. The transformation from relative
to absolute is straightforward and requires nothing but simple matrix multiplication.
However, the transformation from absolute to the relative is slightly more involved and
requires a solution of a simple system of linear equations. Wulfric implements a function
that computes relative coordinates of arbitrary ``vector`` with respect to the arbitrary
non-degenerate ``basis``.

.. doctest::

    >>> basis = [[2, 0, 0], [0, 4, 0], [0, 0, 8]]
    >>> vector = [1, 1, 1]
    >>> wulf.geometry.absolute_to_relative(vector, basis)
    array([0.5  , 0.25 , 0.125])


Pretty array printing
=====================

It just looks nice and easier to debug for the human eye, when printed to the console.
This function can take any numerical 2D or 1D array and print it in a nice
format. It provides custom formatting and color highlights:

.. hint::

    For color highlights pass ``highlight = True`` to the function.
    For color highlights to work, the terminal must support |ANSI|_ escape sequences.

    It highlights positive values in red, negative values in blue, zero values in green.
    Complex and real parts of complex numbers are highlighted separately.


Real-valued array
-----------------

.. doctest::

    >>> array = [[1, 2], [3, 4], [5, 6]]
    >>> wulf.print_2d_array(array)
    ┌──────┬──────┐
    │ 1.00 │ 2.00 │
    ├──────┼──────┤
    │ 3.00 │ 4.00 │
    ├──────┼──────┤
    │ 5.00 │ 6.00 │
    └──────┴──────┘
    >>> wulf.print_2d_array([[0, 1., -0.],[1, 1, 1]])
    ┌──────┬──────┬──────┐
    │ 0.00 │ 1.00 │ 0.00 │
    ├──────┼──────┼──────┤
    │ 1.00 │ 1.00 │ 1.00 │
    └──────┴──────┴──────┘

Custom formatting
-----------------

.. doctest::

    >>> wulf.print_2d_array(array, fmt="10.2f")
    ┌────────────┬────────────┐
    │       1.00 │       2.00 │
    ├────────────┼────────────┤
    │       3.00 │       4.00 │
    ├────────────┼────────────┤
    │       5.00 │       6.00 │
    └────────────┴────────────┘
    >>> wulf.print_2d_array(array, fmt=".2f")
    ┌──────┬──────┐
    │ 1.00 │ 2.00 │
    ├──────┼──────┤
    │ 3.00 │ 4.00 │
    ├──────┼──────┤
    │ 5.00 │ 6.00 │
    └──────┴──────┘

No borders
----------

.. doctest::

    >>> wulf.print_2d_array(array, borders=False)
     1.00 2.00
     3.00 4.00
     5.00 6.00

Shift
-----

.. doctest::

    >>> wulf.print_2d_array(array, shift=3)
       ┌──────┬──────┐
       │ 1.00 │ 2.00 │
       ├──────┼──────┤
       │ 3.00 │ 4.00 │
       ├──────┼──────┤
       │ 5.00 │ 6.00 │
       └──────┴──────┘

Scientific notation
-------------------

.. doctest::

    >>> array = [[1, 2], [3, 4], [52414345345, 6]]
    >>> wulf.print_2d_array(array, fmt="10.2E")
    ┌────────────┬────────────┐
    │   1.00E+00 │   2.00E+00 │
    ├────────────┼────────────┤
    │   3.00E+00 │   4.00E+00 │
    ├────────────┼────────────┤
    │   5.24E+10 │   6.00E+00 │
    └────────────┴────────────┘

Complex-valued array
--------------------

.. doctest::

    >>> array = [[1, 2 + 1j], [3, 4], [52, 6]]
    >>> wulf.print_2d_array(array)
    ┌───────┬──────────────┐
    │  1.00 │ 2.00 + i1.00 │
    ├───────┼──────────────┤
    │  3.00 │ 4.00         │
    ├───────┼──────────────┤
    │ 52.00 │ 6.00         │
    └───────┴──────────────┘
    >>> wulf.print_2d_array(array, fmt="4.2E")
    ┌──────────┬──────────────────────┐
    │ 1.00E+00 │ 2.00E+00 + i1.00E+00 │
    ├──────────┼──────────────────────┤
    │ 3.00E+00 │ 4.00E+00             │
    ├──────────┼──────────────────────┤
    │ 5.20E+01 │ 6.00E+00             │
    └──────────┴──────────────────────┘
    >>> array = [[1, 2 - 1j], [3, 4], [52, 6]]
    >>> wulf.print_2d_array(array)
    ┌───────┬──────────────┐
    │  1.00 │ 2.00 - i1.00 │
    ├───────┼──────────────┤
    │  3.00 │ 4.00         │
    ├───────┼──────────────┤
    │ 52.00 │ 6.00         │
    └───────┴──────────────┘

Complex-valued array with real part equal to zero
-------------------------------------------------

.. doctest::

    >>> array = [[1, 1j], [3, 4], [52, 6]]
    >>> wulf.print_2d_array(array)
    ┌───────┬──────────────┐
    │  1.00 │      + i1.00 │
    ├───────┼──────────────┤
    │  3.00 │ 4.00         │
    ├───────┼──────────────┤
    │ 52.00 │ 6.00         │
    └───────┴──────────────┘

Empty cells
-----------

.. doctest::

    >>> array = [[1, 2], [3, 4], [5, 6]]
    >>> array[1][1] = None
    >>> wulf.print_2d_array(array)
    ┌──────┬──────┐
    │ 1.00 │ 2.00 │
    ├──────┼──────┤
    │ 3.00 │      │
    ├──────┼──────┤
    │ 5.00 │ 6.00 │
    └──────┴──────┘
    >>> array[1][0] = None
    >>> wulf.print_2d_array(array)
    ┌──────┬──────┐
    │ 1.00 │ 2.00 │
    ├──────┼──────┤
    │      │      │
    ├──────┼──────┤
    │ 5.00 │ 6.00 │
    └──────┴──────┘
    >>> array[0][1] = None
    >>> array[2][1] = None
    >>> wulf.print_2d_array(array)
    ┌──────┬──┐
    │ 1.00 │  │
    ├──────┼──┤
    │      │  │
    ├──────┼──┤
    │ 5.00 │  │
    └──────┴──┘

Empty arrays
------------

.. doctest::

    >>> wulf.print_2d_array([])
    None
    >>> wulf.print_2d_array([[]])
    None

Long numbers
------------

.. doctest::

    >>> array = [[1, 2], [3, 4], [52414345345, 6]]
    >>> wulf.print_2d_array(array)
    ┌────────────────┬──────┐
    │           1.00 │ 2.00 │
    ├────────────────┼──────┤
    │           3.00 │ 4.00 │
    ├────────────────┼──────┤
    │ 52414345345.00 │ 6.00 │
    └────────────────┴──────┘

Headers and footers
-------------------

.. doctest::

    >>> array = [[1, 2], [3, 4], [5, 6]]
    >>> wulf.print_2d_array(array, header_row=["a", "b"])
    ┌──────┬──────┐
    │    a │    b │
    ├──────┼──────┤
    │ 1.00 │ 2.00 │
    ├──────┼──────┤
    │ 3.00 │ 4.00 │
    ├──────┼──────┤
    │ 5.00 │ 6.00 │
    └──────┴──────┘
    >>> wulf.print_2d_array(array, footer_row=["c", "d"])
    ┌──────┬──────┐
    │ 1.00 │ 2.00 │
    ├──────┼──────┤
    │ 3.00 │ 4.00 │
    ├──────┼──────┤
    │ 5.00 │ 6.00 │
    ├──────┼──────┤
    │    c │    d │
    └──────┴──────┘
    >>> wulf.print_2d_array(array, header_column=["a", "b", "c"])
    ┌───┬──────┬──────┐
    │ a │ 1.00 │ 2.00 │
    ├───┼──────┼──────┤
    │ b │ 3.00 │ 4.00 │
    ├───┼──────┼──────┤
    │ c │ 5.00 │ 6.00 │
    └───┴──────┴──────┘
    >>> wulf.print_2d_array(array, footer_column=["a", "b", "c"])
    ┌──────┬──────┬───┐
    │ 1.00 │ 2.00 │ a │
    ├──────┼──────┼───┤
    │ 3.00 │ 4.00 │ b │
    ├──────┼──────┼───┤
    │ 5.00 │ 6.00 │ c │
    └──────┴──────┴───┘
    >>> wulf.print_2d_array(array, header_column=["a", "B", "c"], header_row = ["", "A", "B"])
    ┌───┬──────┬──────┐
    │   │    A │    B │
    ├───┼──────┼──────┤
    │ a │ 1.00 │ 2.00 │
    ├───┼──────┼──────┤
    │ B │ 3.00 │ 4.00 │
    ├───┼──────┼──────┤
    │ c │ 5.00 │ 6.00 │
    └───┴──────┴──────┘
    >>> wulf.print_2d_array(array, header_column=["a", "B", "c"], header_row = ["corner", "A", "B"])
    ┌────────┬──────┬──────┐
    │ corner │    A │    B │
    ├────────┼──────┼──────┤
    │      a │ 1.00 │ 2.00 │
    ├────────┼──────┼──────┤
    │      B │ 3.00 │ 4.00 │
    ├────────┼──────┼──────┤
    │      c │ 5.00 │ 6.00 │
    └────────┴──────┴──────┘
    >>> wulf.print_2d_array(array, header_column=["a", "B", "c"], header_row = ["", "A", "B",""], footer_row = ["","c","d",""], footer_column=["c","d","e"])
    ┌───┬──────┬──────┬───┐
    │   │    A │    B │   │
    ├───┼──────┼──────┼───┤
    │ a │ 1.00 │ 2.00 │ c │
    ├───┼──────┼──────┼───┤
    │ B │ 3.00 │ 4.00 │ d │
    ├───┼──────┼──────┼───┤
    │ c │ 5.00 │ 6.00 │ e │
    ├───┼──────┼──────┼───┤
    │   │    c │    d │   │
    └───┴──────┴──────┴───┘
    >>> array = [[1, 2], [3, 4], [5, 6+1j]]
    >>> wulf.print_2d_array(array, header_row=["a", "b"])
    ┌──────┬──────────────┐
    │    a │            b │
    ├──────┼──────────────┤
    │ 1.00 │ 2.00         │
    ├──────┼──────────────┤
    │ 3.00 │ 4.00         │
    ├──────┼──────────────┤
    │ 5.00 │ 6.00 + i1.00 │
    └──────┴──────────────┘
    >>> wulf.print_2d_array(array, header_row=["a", "b"], fmt="^.2f")
    ┌──────┬──────────────┐
    │  a   │      b       │
    ├──────┼──────────────┤
    │ 1.00 │ 2.00         │
    ├──────┼──────────────┤
    │ 3.00 │ 4.00         │
    ├──────┼──────────────┤
    │ 5.00 │ 6.00 + i1.00 │
    └──────┴──────────────┘


References
==========
.. [1] Grosse-Kunstleve, R.W., Sauter, N.K. and Adams, P.D., 2004.
    Numerically stable algorithms for the computation of reduced unit cells.
    Acta Crystallographica Section A: Foundations of Crystallography,
    60(1), pp.1-6.
