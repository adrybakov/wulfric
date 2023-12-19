.. _user-guide_module_plotting:

.. currentmodule:: wulfric

********
Plotting
********

For the full reference see :ref:`api_crystal-plotting`

More examples of the plots with the code snippets can be found in the
:ref:`library_bravais-lattices` guide.

.. note::

    The plotting is written for the :py:class:`.Lattice` and consequently
    available for it's child: :py:class`.Crystal` class.

Import
======

.. doctest::

    >>> # Exact import
    >>> from wulfric.lattice_plotter import MatplotlibBackend, PlotlyBackend
    >>> # Recommended import
    >>> from wulfric import MatplotlibBackend, PlotlyBackend


For the examples in this page we need additional import and some predefined variables:

.. doctest::

    >>> from wulfric import HEX
    >>> lattice = HEX(2, 1)



Creation
========

Each backend is created as any other object in Python:

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

The typical workflow consist in plotting one or several lattices and then
showing or saving the figure:

.. doctest::

    >>> pb.plot(lattice, kind="brillouin", label="Brillouin zone", color="red") # doctest: +SKIP
    >>> pb.plot(lattice, kind="kpath", label="K-path", color="black") # doctest: +SKIP
    >>> pb.save('hex_lattice.html') # doctest: +SKIP
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

    >>> mb.plot(lattice, kind="brillouin", label="Brillouin zone", color="red") # doctest: +SKIP
    >>> mb.plot(lattice, kind="kpath", label="K-path", color="black") # doctest: +SKIP
    >>> mb.save('hex_lattice.png') # doctest: +SKIP
    >>> mb.show() # doctest: +SKIP
