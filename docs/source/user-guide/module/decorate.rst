.. _user-guide_module_decorate:

******************
Decoration of data
******************

For the full reference see :ref:`api_decorate`.

.. currentmodule:: wulfric

This module contains functions to decorate data for plotting or printing.
It does not fall into the scope of intended functionality of the package,
but is included for convenience.

Import
======

.. doctest::

    >>> # Exact import
    >>> from wulfric.decorate.array import print_2d_array
    >>> # Explicit import
    >>> from wulfric.decorate import print_2d_array
    >>> # Recommended import
    >>> from wulfric import print_2d_array

2D arrays
=========

This function can take any numerical 2D or 1D array and print it in a nice
format. It is useful for debugging and printing of results.


It provides custom formatting, colour highlighting:

.. hint::

    For colour highlighting pass ``highlight=True`` to the function.
    For colour highlighting to work, the terminal must support |ANSI|_ escape sequences.

    It highlights positive values in red, negative values in blue, zero values in green.
    Complex and real parts of complex numbers are highlighted separately.


Real-valued array
-----------------

.. doctest::

    >>> array = [[1, 2], [3, 4], [5, 6]]
    >>> print_2d_array(array)
    ┌──────┬──────┐
    │ 1.00 │ 2.00 │
    ├──────┼──────┤
    │ 3.00 │ 4.00 │
    ├──────┼──────┤
    │ 5.00 │ 6.00 │
    └──────┴──────┘
    >>> print_2d_array([[0, 1., -0.],[1, 1, 1]])
    ┌──────┬──────┬──────┐
    │ 0.00 │ 1.00 │ 0.00 │
    ├──────┼──────┼──────┤
    │ 1.00 │ 1.00 │ 1.00 │
    └──────┴──────┴──────┘

Custom formatting
-----------------

.. doctest::

    >>> print_2d_array(array, fmt="10.2f")
    ┌────────────┬────────────┐
    │       1.00 │       2.00 │
    ├────────────┼────────────┤
    │       3.00 │       4.00 │
    ├────────────┼────────────┤
    │       5.00 │       6.00 │
    └────────────┴────────────┘
    >>> print_2d_array(array, fmt=".2f")
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

    >>> print_2d_array(array, borders=False)
     1.00 2.00
     3.00 4.00
     5.00 6.00

Shift
-----

.. doctest::

    >>> print_2d_array(array, shift=3)
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
    >>> print_2d_array(array, fmt="10.2E")
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
    >>> print_2d_array(array)
    ┌───────┬──────────────┐
    │  1.00 │ 2.00 + i1.00 │
    ├───────┼──────────────┤
    │  3.00 │ 4.00         │
    ├───────┼──────────────┤
    │ 52.00 │ 6.00         │
    └───────┴──────────────┘
    >>> print_2d_array(array, fmt="4.2E")
    ┌──────────┬──────────────────────┐
    │ 1.00E+00 │ 2.00E+00 + i1.00E+00 │
    ├──────────┼──────────────────────┤
    │ 3.00E+00 │ 4.00E+00             │
    ├──────────┼──────────────────────┤
    │ 5.20E+01 │ 6.00E+00             │
    └──────────┴──────────────────────┘
    >>> array = [[1, 2 - 1j], [3, 4], [52, 6]]
    >>> print_2d_array(array)
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
    >>> print_2d_array(array)
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
    >>> print_2d_array(array)
    ┌──────┬──────┐
    │ 1.00 │ 2.00 │
    ├──────┼──────┤
    │ 3.00 │      │
    ├──────┼──────┤
    │ 5.00 │ 6.00 │
    └──────┴──────┘
    >>> array[1][0] = None
    >>> print_2d_array(array)
    ┌──────┬──────┐
    │ 1.00 │ 2.00 │
    ├──────┼──────┤
    │      │      │
    ├──────┼──────┤
    │ 5.00 │ 6.00 │
    └──────┴──────┘
    >>> array[0][1] = None
    >>> array[2][1] = None
    >>> print_2d_array(array)
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

    >>> print_2d_array([])
    None
    >>> print_2d_array([[]])
    None

Long numbers
------------

.. doctest::

    >>> array = [[1, 2], [3, 4], [52414345345, 6]]
    >>> print_2d_array(array)
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
    >>> print_2d_array(array, header_row=["a", "b"])
    ┌──────┬──────┐
    │    a │    b │
    ├──────┼──────┤
    │ 1.00 │ 2.00 │
    ├──────┼──────┤
    │ 3.00 │ 4.00 │
    ├──────┼──────┤
    │ 5.00 │ 6.00 │
    └──────┴──────┘
    >>> print_2d_array(array, footer_row=["c", "d"])
    ┌──────┬──────┐
    │ 1.00 │ 2.00 │
    ├──────┼──────┤
    │ 3.00 │ 4.00 │
    ├──────┼──────┤
    │ 5.00 │ 6.00 │
    ├──────┼──────┤
    │    c │    d │
    └──────┴──────┘
    >>> print_2d_array(array, header_column=["a", "b", "c"])
    ┌───┬──────┬──────┐
    │ a │ 1.00 │ 2.00 │
    ├───┼──────┼──────┤
    │ b │ 3.00 │ 4.00 │
    ├───┼──────┼──────┤
    │ c │ 5.00 │ 6.00 │
    └───┴──────┴──────┘
    >>> print_2d_array(array, footer_column=["a", "b", "c"])
    ┌──────┬──────┬───┐
    │ 1.00 │ 2.00 │ a │
    ├──────┼──────┼───┤
    │ 3.00 │ 4.00 │ b │
    ├──────┼──────┼───┤
    │ 5.00 │ 6.00 │ c │
    └──────┴──────┴───┘
    >>> print_2d_array(array, header_column=["a", "B", "c"], header_row = ["", "A", "B"])
    ┌───┬──────┬──────┐
    │   │    A │    B │
    ├───┼──────┼──────┤
    │ a │ 1.00 │ 2.00 │
    ├───┼──────┼──────┤
    │ B │ 3.00 │ 4.00 │
    ├───┼──────┼──────┤
    │ c │ 5.00 │ 6.00 │
    └───┴──────┴──────┘
    >>> print_2d_array(array, header_column=["a", "B", "c"], header_row = ["corner", "A", "B"])
    ┌────────┬──────┬──────┐
    │ corner │    A │    B │
    ├────────┼──────┼──────┤
    │      a │ 1.00 │ 2.00 │
    ├────────┼──────┼──────┤
    │      B │ 3.00 │ 4.00 │
    ├────────┼──────┼──────┤
    │      c │ 5.00 │ 6.00 │
    └────────┴──────┴──────┘
    >>> print_2d_array(array, header_column=["a", "B", "c"], header_row = ["", "A", "B",""], footer_row = ["","c","d",""], footer_column=["c","d","e"])
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
    >>> print_2d_array(array, header_row=["a", "b"])
    ┌──────┬──────────────┐
    │    a │            b │
    ├──────┼──────────────┤
    │ 1.00 │ 2.00         │
    ├──────┼──────────────┤
    │ 3.00 │ 4.00         │
    ├──────┼──────────────┤
    │ 5.00 │ 6.00 + i1.00 │
    └──────┴──────────────┘
    >>> print_2d_array(array, header_row=["a", "b"], fmt="^.2f")
    ┌──────┬──────────────┐
    │  a   │      b       │
    ├──────┼──────────────┤
    │ 1.00 │ 2.00         │
    ├──────┼──────────────┤
    │ 3.00 │ 4.00         │
    ├──────┼──────────────┤
    │ 5.00 │ 6.00 + i1.00 │
    └──────┴──────────────┘
