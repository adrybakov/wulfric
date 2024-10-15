.. module:: wulfric

.. _api:

*************
API reference
*************

:Release: |version|

The reference manual describes modules and their objects,
which may be used for the postprocessing.
The main interface to the package may be imported as

.. code-block:: python

   import wulfric as wulf

In the examples across the documentation it is expected to be imported in that way.


.. toctree::
   :caption: Core elements
   :maxdepth: 1

   cell
   lattice
   bravais-lattice
   kpoints
   atom
   crystal

.. toctree::
   :caption: Supplementary elements
   :maxdepth: 1

   identify
   io
   geometry
   numerical
   decorate
   constants
   exceptions

.. _api_crystal-plotting:

.. toctree::
   :caption: Plotting
   :maxdepth: 1

   plotly-backend
   matplotlib-backend
