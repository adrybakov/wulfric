*******
Wulfric
*******

Crystal, Lattice, Atoms, K-path.

.. image:: https://badge.fury.io/py/wulfric.svg
  :target: https://badge.fury.io/py/wulfric/

.. image:: https://readthedocs.org/projects/wulfric/badge/?version=latest
  :target: https://wulfric.org/en/latest/?badge=latest
  :alt: Documentation Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :target: https://github.com/psf/black/

.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=505050
  :target: https://pycqa.github.io/isort/

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
  :target: https://www.gnu.org/licenses/gpl-3.0

.. image:: https://results.pre-commit.ci/badge/github/adrybakov/wulfric/main.svg
  :target: https://results.pre-commit.ci/latest/github/adrybakov/wulfric/main
  :alt: pre-commit.ci status

Wulfric is a python package for the crystal structures. It uses a simple concepts of
``cell`` and ``atoms`` and provides a set of functions for the manipulations with them.

The functionality of wulfric includes (but not limited to):

* Calculation of Bravais lattice type and variation.

* Automatic choice of the Kpoints and K-path based on Bravais lattice types.

* Set of useful functions for manipulations with cells and crystalls (cell + atoms).

* Implementation of LePage and Niggli reduction algorithms.

Please visit an extensive documentation on `https://wulfric.org`_ to find out more.


Installation
============

To install wulfric, run (you may need to use ``pip3``):

.. code-block:: console

  pip install wulfric

To install with optional visualization capabilities, run (you may need to use ``pip3``):

.. code-block:: console

  pip install "wulfric[visual]"
