.. _user-guide_usage_kpoints:

********
K points
********

On this page we describe one of the main usage of wulfric - automatic generation of
high symmetry points for any given cell.

For the full technical reference see :py:class:`.Kpoints` and :ref:`api_cell_kpoints`.

In the examples of this page we assume that wulfric is imported as

.. doctest::

  >>> import wulfric


K-points data
=============

If you only need the simple data about the high symmetry points and nothing else, then
use

.. doctest::

    >>> cell = wulfric.cell.get_example_cell_SC("BCT")
    >>> coordinates, names, labels, path = wulfric.cell.get_hs_data(cell)
    >>> path
    'G-X-M-G-Z-P-N-Z1-M|X-P'
    >>> names
    ['G', 'M', 'N', 'P', 'X', 'Z', 'Z1']
    >>> labels
    ['$\\Gamma$', 'M', 'N', 'P', 'X', 'Z', 'Z$_1$']
    >>> for coordinate in coordinates:
    ...   print(coordinate)
    ...
    [0. 0. 0.]
    [-0.5  0.5  0.5]
    [0.  0.5 0. ]
    [0.25 0.25 0.25]
    [0.  0.  0.5]
    [ 0.36111111  0.36111111 -0.36111111]
    [-0.36111111  0.63888889  0.36111111]

This function will return ``names`` and ``labels`` of high symmetry kpoints. Names are used in the
specification of the ``path``, while labels are better suited for plotting. For instance,
if ``'$\\Gamma$'`` is used with |matplotlib|_, then it produces a nice "Γ" letter.

For the strict definition of how the path is specified see
:ref:`user-guide_usage_key-concepts_kpath`.

By default coordinates are relative to the reciprocal cell, defined by ``cell``. Use
``return_relative = False``, to obtain absolute coordinates instead.

Kpoints class
=============

A convenient way to manage kpoints and kpath for calculations or for plotting is
implemented with the :py:class:`.Kpoints` class.

Creation
--------

Usually it is created from some ``cell``:

.. doctest::

    >>> cell = wulfric.cell.get_example_cell_SC("CUB")
    >>> kp = wulfric.Kpoints.from_cell(cell)
    >>> kp.hs_names
    ['G', 'M', 'R', 'X']

However, it could be created explicitly as well:

.. doctest::

    >>> rcell = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    >>> names = ["G", "X"]
    >>> coordinates = [[0, 0, 0], [0.5, 0, 0]]
    >>> labels = [R"$\Gamma$", "X"]
    >>> kp = wulfric.Kpoints(rcell, names=names, coordinates=coordinates, labels=labels)
    >>> kp.hs_names
    ['G', 'X']

For the full list of constructor's parameters see :py:class:`.Kpoints`.

High-symmetry points
--------------------

Information about high symmetry points is accessible through the following properties:

* :py:attr:`.Kpoints.hs_names`

List of names of high symmetry points.

.. doctest::

    >>> kp.hs_names
    ['G', 'X']

* :py:attr:`.Kpoints.hs_coordinates`

Dictionary of coordinates of high symmetry points.

.. doctest::

    >>> kp.hs_coordinates
    {'G': array([0, 0, 0]), 'X': array([0.5, 0. , 0. ])}

* :py:attr:`.Kpoints.hs_labels`

Dictionary of labels of high symmetry points. Usually used for plotting.

.. doctest::

    >>> kp.hs_labels
    {'G': '$\\Gamma$', 'X': 'X'}

.. note::
    Names of high symmetry points have to be unique.

Adding a point
--------------

.. doctest::

    >>> kp.add_hs_point(name="M", coordinate=[0.5, 0.5, 0], label="M")
    >>> kp.hs_names
    ['G', 'X', 'M']
    >>> kp.hs_coordinates
    {'G': array([0, 0, 0]), 'X': array([0.5, 0. , 0. ]), 'M': array([0.5, 0.5, 0. ])}
    >>> kp.hs_labels
    {'G': '$\\Gamma$', 'X': 'X', 'M': 'M'}

Getting summary of high-symmetry points
---------------------------------------

In order to have a summary of the high symmetry pints the predefined method
:py:meth:`.Kpoints.hs_table` may be used:

.. doctest::

    >>> kp = wulfric.Kpoints.from_cell(wulfric.cell.get_example_cell_SC("FCC"))
    >>> print(kp.hs_table())
    Name       rel_b1      rel_b2      rel_b3          k_x         k_y         k_z
    G      0.00000000  0.00000000  0.00000000   0.00000000  0.00000000  0.00000000
    K      0.37500000  0.37500000  0.75000000   1.50000000  1.50000000  0.00000000
    L      0.50000000  0.50000000  0.50000000   1.00000000  1.00000000  1.00000000
    U      0.62500000  0.25000000  0.62500000   0.50000000  2.00000000  0.50000000
    W      0.50000000  0.25000000  0.75000000   1.00000000  2.00000000  0.00000000
    X      0.50000000  0.00000000  0.50000000   0.00000000  2.00000000  0.00000000

.. _user-guide_usage_kpoints-path:

Path
----

The path is the route in the reciprocal space, defined by the high symmetry points.

We use a specific format in the package that is described in
:ref:`user-guide_usage_key-concepts_kpath`.

.. doctest::

    >>> # Create a Kpoints instance
    >>> rcell = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    >>> names = ["G", "K", "X", "R"]
    >>> coordinates = [[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0], [0.5, 0.5, 0.5]]
    >>> labels = ["$\Gamma$", "K", "X", "R"]
    >>> kp = wulfric.Kpoints(rcell, names=names, coordinates=coordinates, labels=labels)
    >>> # Default path is constructed from the list of high symmetry points
    >>> kp.path
    [['G', 'K', 'X', 'R']]
    >>> # Only the names from Kpoints.hs_names are allowed to be used in the path
    >>> # Next line causes an ValueError, because high symmetry point "S" is not defined
    >>> kp.path = "G-K-X|R-S"
    Traceback (most recent call last):
    ...
    ValueError: Point 'S' is not defined. Defined points are:
      G : [0 0 0]
      K : [0.5 0.5 0. ]
      X : [0.5 0.  0. ]
      R : [0.5 0.5 0.5]
    >>> # Now we split path into two subpaths
    >>> kp.path = "G-K-X|R-G"
    >>> kp.path
    [['G', 'K', 'X'], ['R', 'G']]
    >>> # We can add a point to de used in the path
    >>> kp.add_hs_point(name="S", coordinate=[0.5, 0.5, 0.5], label="S")
    >>> # Now it is possible to use "S" it in the path
    >>> kp.path = "G-K-X|R-S"
    >>> kp.path
    [['G', 'K', 'X'], ['R', 'S']]
    >>> # The path_string property returns the path in the string format
    >>> kp.path_string
    'G-K-X|R-S'

.. note::

    Internally wulfric stores the path as a list of subpaths, where each subpath
    is a list of high symmetry point's names. This format is also correct for assigning
    the :py:attr:`.Kpoints.path` attribute.

Configuration
-------------

The amount of kpoints to be generated between each pair of high symmetry points in the path
is controlled by the :py:attr:`.Kpoints.n` property.

.. doctest::

    >>> # Default value is 100
    >>> kp.n
    100
    >>> kp.n = 10
    >>> kp.n
    10


Once the configuration of the Kpoints is done, it can be used for calculation or plotting.

Calculation
-----------

There is one method suitable for calculation: :py:meth:`.Kpoints.points`. It is an array
of all generated kpoints. For each pair of high symmetry points it generates
:py:attr:`.Kpoints.n` points between them. The first and the last points are always
the high symmetry points of this section of the path.

.. doctest::

    >>> rcell = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    >>> names = ["G", "K", "X"]
    >>> coordinates = [[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0]]
    >>> labels = ["$\Gamma$", "K", "X"]
    >>> kp = wulfric.Kpoints(rcell, names=names, coordinates=coordinates, labels=labels, n=4)
    >>> kp.points()
    array([[0. , 0. , 0. ],
           [0.1, 0.1, 0. ],
           [0.2, 0.2, 0. ],
           [0.3, 0.3, 0. ],
           [0.4, 0.4, 0. ],
           [0.5, 0.5, 0. ],
           [0.5, 0.5, 0. ],
           [0.5, 0.4, 0. ],
           [0.5, 0.3, 0. ],
           [0.5, 0.2, 0. ],
           [0.5, 0.1, 0. ],
           [0.5, 0. , 0. ]])

.. hint::
    For each section the last point is repeated twice, because it is the first point
    of the next section of the path.

    .. code-block:: python

        array([[0. , 0. , 0. ], # <--- Gamma
               [0.1, 0.1, 0. ],
               [0.2, 0.2, 0. ],
               [0.3, 0.3, 0. ],
               [0.4, 0.4, 0. ],
               [0.5, 0.5, 0. ], # <--- K
               [0.5, 0.5, 0. ], # <--- K
               [0.5, 0.4, 0. ],
               [0.5, 0.3, 0. ],
               [0.5, 0.2, 0. ],
               [0.5, 0.1, 0. ],
               [0.5, 0. , 0. ]]) # <--- X

Plotting
--------

For plotting there is one property :py:attr:`.Kpoints.labels` and two methods
(:py:meth:`.Kpoints.ticks`, :py:meth:`.Kpoints.flatten_points`). Two of them are for the
high symmetry points and describe the labels and position of ticks on the x-axis:

.. doctest::

    >>> kp.labels
    ['$\\Gamma$', 'K', 'X']
    >>> import numpy as np
    >>> np.around(kp.ticks(), decimals=4)
    array([0.    , 0.7071, 1.2071])

The third property gives the coordinates of the :py:meth:`.Kpoints.points` for the plot:

.. doctest::

    >>> for point in kp.flatten_points():
    ...     print(round(point, 4))
    ...
    0.0
    0.1414
    0.2828
    0.4243
    0.5657
    0.7071
    0.7071
    0.8071
    0.9071
    1.0071
    1.1071
    1.2071

.. note::
    Those coordinates are directly corresponds to the k-points from the previous subsection.

    .. code-block:: python

        0.0    # <--- Gamma
        0.1414
        0.2828
        0.4243
        0.5657
        0.7071 # <--- K
        0.7071 # <--- K
        0.8071
        0.9071
        1.0071
        1.1071
        1.2071 # <--- X

.. hint::

    Repeated :py:meth:`.Kpoints.points` or :py:meth:`.Kpoints.flatten_points` can be used
    to restore the position of high symmetry points in the path.
