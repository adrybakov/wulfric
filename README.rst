*******
Wulfric
*******

Crystal, Lattice, Atoms, K-path.

.. image:: https://badge.fury.io/py/wulfric.svg
  :target: https://badge.fury.io/py/wulfric/

.. image:: https://readthedocs.org/projects/wulfric/badge/?version=latest
  :target: https://wulfric.org/en/latest/?badge=latest
  :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
  :target: https://www.gnu.org/licenses/gpl-3.0

.. image:: https://results.pre-commit.ci/badge/github/adrybakov/wulfric/main.svg
  :target: https://results.pre-commit.ci/latest/github/adrybakov/wulfric/main
  :alt: pre-commit.ci status


****************
What is Wulfric?
****************

Wulfric is a python package for the crystal structures. It uses concepts of
``cell``, ``atoms``, ``k-points`` and provides a simple skeleton for the user to built on
(see `Key concepts <https://docs.wulfric.org/en/latest/user-guide/usage/key-concepts.html>`_).

The functionality of Wulfric includes (but not limited to):

*   Choice of the conventional and primitive cells
    (`Which Cell? <https://docs.wulfric.org/en/latest/user-guide/conventions/which-cell.html>`_).

*   Automatic choice of the `Kpoints <https://docs.wulfric.org/en/latest/user-guide/usage/kpoints.html>`_
    and k-path for all `Bravais lattice types <https://docs.wulfric.org/en/latest/user-guide/conventions/bravais-lattices/index.html>`_
    and space groups.

*   Full support for `Setyawan and Curtarolo (SC) <https://docs.wulfric.org/en/latest/user-guide/conventions/bravais-lattices/2_sc/index.html>`_ convention.

*   Full support for `Hinuma, Pizzi, Kumagai, Oba, Tanaka (HPKOT) <https://docs.wulfric.org/en/latest/user-guide/conventions/bravais-lattices/1_hpkot/index.html>`_ convention.

*   `Visualization <https://docs.wulfric.org/en/latest/user-guide/usage/visualization/index.html>`_ of `cells <https://docs.wulfric.org/en/latest/user-guide/usage/visualization/plot_2_cell.html>`_, `atoms <https://docs.wulfric.org/en/latest/user-guide/usage/visualization/plot_5_atoms.html>`_, `lattices <https://docs.wulfric.org/en/latest/user-guide/usage/visualization/plot_3_lattice.html>`_, `k-path and k-points <https://docs.wulfric.org/en/latest/user-guide/usage/visualization/plot_6_kpath.html>`_.

*   Common `Manipulations with cell <https://docs.wulfric.org/en/latest/user-guide/usage/cell.html>`_ and `Manipulations with crystal <https://docs.wulfric.org/en/latest/user-guide/usage/crystal.html>`_.

*************
Documentation
*************

Extensive documentation is available at `wulfric.org <https://wulfric.org>`_.

*   For code examples see `User guide <https://docs.wulfric.org/en/latest/user-guide/index.html>`_.
*   For full public API see `API <https://docs.wulfric.org/en/latest/api/index.html>`_.
*   To get some support and ask questions see `User support <https://docs.wulfric.org/en/latest/support.html>`_.
*   To understand how transformations and rotations are performed in Wulfric; how the cells,
    atom positions, and k-points are stored see `Basic notation <https://docs.wulfric.org/en/latest/user-guide/conventions/basic-notation.html>`_ and
    `Key concepts <https://docs.wulfric.org/en/latest/user-guide/usage/key-concepts.html>`_.
*   To understand the difference between various cells see
    `Which cell? <https://docs.wulfric.org/en/latest/user-guide/conventions/which-cell.html>`_.
*   To check examples of what Wulfric can visualize see
    `Visualization <https://docs.wulfric.org/en/latest/user-guide/usage/visualization/index.html>`_.
*   For summary of releases see `Release notes <https://docs.wulfric.org/en/latest/release-notes/index.html>`_.


************
Installation
************

To install Wulfric, run (you may need to use ``pip3``):

.. code-block:: console

  pip install wulfric

To install with visualization capabilities, run (you may need to use ``pip3``):

.. code-block:: console

  pip install "wulfric[visual]"

*******
License
*******

The source code of Wulfric is licensed under the  GNU General Public
License (GPL-3.0). See the `"LICENSE" file <https://github.com/adrybakov/wulfric/blob/main/LICENSE>`_ in the `Wulfric's repository <https://github.com/adrybakov/wulfric>`_

In addition, if you use Wulfric in the scientific publication, cite the package as

.. code-block:: text

  A. Rybakov, Wulfric, 2023, [software] https://github.com/adrybakov/wulfric.

.. code-block:: LaTeX

  @misc{Rybakov2023Wulfric,
    author = "Rybakov, A.",
    title  = "Wulfric",
    note   = "[software] \url{https://github.com/adrybakov/wulfric}",
    year   = "2023"}


For the detailed guide on how to cite the papers on which Wulfric depends
see `Citation guide <https://docs.wulfric.org/en/latest/cite.html>`_.
