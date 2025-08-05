.. _user-guide_usage_visualization:


*************
Visualization
*************

For the full technical reference see :py:class:`.PlotlyEngine`.

More examples of the plots with the code snippets can be found in the
:ref:`user-guide_conventions_bravais-lattices` guide. All interactive plots there are
created with wulfric.

First one need to create an instance of the plotting engine as

.. doctest::

    >>> import wulfric
    >>> pe = wulfric.PlotlyEngine()

The creation of the plotting engine can take one optional argument: ``fig``:

.. doctest::

    >>> from plotly import graph_objects as go # doctest: +SKIP
    >>> fig = go.Figure() # doctest: +SKIP
    >>> pe = PlotlyEngine(fig=fig) # doctest: +SKIP

The typical usage scenario is to plot one or several cells and then
show or save the figure:

.. doctest::

    >>> cell = wulfric.cell.HEX(2, 1)
    >>> pe.plot_brillouin(cell,  legend_label="Brillouin zone", color="red") # doctest: +SKIP
    >>> pe.plot_kpath(cell,  legend_label="K-path", color="black") # doctest: +SKIP
    >>> pe.save('hex_cell.html') # doctest: +SKIP
    >>> pe.show() # doctest: +SKIP
