.. _user-guide_usage_visualization:


*************
Visualization
*************

.. note::

    There are much better visualization software exist and wulfric is not intended to be used
    as one. simple visualization capabilities were written historically for the quick debugging
    and later on used for the automatic creation of the examples in the
    :ref:`user-guide_conventions_bravais-lattices` pages.

For the full technical reference see :ref:`api_visualization`

More examples of the plots with the code snippets can be found in the
:ref:`user-guide_conventions_bravais-lattices` guide. All interactive plots there are
created with plotly backend.

In the examples on this page we assume that wulfric is imported as

.. doctest::

  >>> import wulfric as wulf

And an example cell of the hexagonal lattice is created as

.. doctest::

    >>> cell = wulf.cell.HEX(2, 1)



Each backend is invoked as any other object in Python:

.. doctest::

    >>> mb = MatplotlibBackend() # doctest: +SKIP
    >>> pb = PlotlyBackend() # doctest: +SKIP


Plotting with Plotly
====================

|plotly|_ is considered to be the main plotting backend.

The creation of the plotly backend can take one optional argument: ``fig``:

.. doctest::

    >>> from plotly import graph_objects as go # doctest: +SKIP
    >>> fig = go.Figure() # doctest: +SKIP
    >>> pb = PlotlyBackend(fig=fig) # doctest: +SKIP

The typical usage scenario is to plot one or several cells and then
show or save the figure:

.. doctest::

    >>> pb.plot(cell, kind="brillouin", label="Brillouin zone", color="red") # doctest: +SKIP
    >>> pb.plot(cell, kind="kpath", label="K-path", color="black") # doctest: +SKIP
    >>> pb.save('hex_cell.html') # doctest: +SKIP
    >>> pb.show() # doctest: +SKIP

Plotting with Matplotlib
========================

|matplotlib|_ is considered to be the secondary plotting backend.

The creation of the matplotlib backend can take one optional arguments: ``fig`` and ``ax``:

.. doctest::

    >>> import matplotlib.pyplot as plt # doctest: +SKIP
    >>> fig = plt.figure(figsize=(6, 6)) # doctest: +SKIP
    >>> ax = fig.add_subplot(projection="3d") # doctest: +SKIP
    >>> mb = MatplotlibBackend(fig=fig, ax=ax) # doctest: +SKIP

The typical workflow consist in plotting one or several lattices and then
showing or saving the figure:

.. doctest::

    >>> mb.plot(cell, kind="brillouin", label="Brillouin zone", color="red") # doctest: +SKIP
    >>> mb.plot(cell, kind="kpath", label="K-path", color="black") # doctest: +SKIP
    >>> mb.save('hex_cell.png') # doctest: +SKIP
    >>> mb.show() # doctest: +SKIP
