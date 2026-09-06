# Wulfric

Crystal, Lattice, Atoms, K-path.


[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version](https://badge.fury.io/py/wulfric.svg)](https://badge.fury.io/py/wulfric/)
![Python](https://img.shields.io/pypi/pyversions/wulfric)

[![Documentation Status](https://readthedocs.org/projects/wulfric/badge/?version=latest)](https://wulfric.org/en/latest/?badge=latest)
[![tests (main)](https://github.com/adrybakov/wulfric/actions/workflows/singular-test.yml/badge.svg?branch=main)](https://github.com/adrybakov/wulfric/actions/workflows/singular-test.yml)
[![tests (dev)](https://github.com/adrybakov/wulfric/actions/workflows/singular-test.yml/badge.svg?branch=dev)](https://github.com/adrybakov/wulfric/actions/workflows/singular-test.yml)

## What is Wulfric?

Wulfric is a python package for the crystal structures. It uses concepts of
``cell``, ``atoms``, ``k-points`` and provides a simple skeleton for the user to built on
(see [Key concepts](https://docs.wulfric.org/en/latest/user-guide/usage/key-concepts.html)).

The main features of Wulfric are

*   Choice of the conventional and primitive cells
    ([Which Cell](https://docs.wulfric.org/en/latest/user-guide/conventions/which-cell.html)).

*   Automatic choice of the [Kpoints](https://docs.wulfric.org/en/latest/user-guide/usage/kpoints.html)
    and k-path for all [Bravais lattice types](https://docs.wulfric.org/en/latest/user-guide/conventions/bravais-lattices/index.html)
    and space groups.

*   Full support for [Setyawan and Curtarolo (SC)](https://docs.wulfric.org/en/latest/user-guide/conventions/bravais-lattices/2_sc/index.html) convention.

*   Full support for [Hinuma, Pizzi, Kumagai, Oba, Tanaka (HPKOT)](https://docs.wulfric.org/en/latest/user-guide/conventions/bravais-lattices/1_hpkot/index.html) convention.

*   [Visualization](https://docs.wulfric.org/en/latest/user-guide/usage/visualization/index.html) of [cells](https://docs.wulfric.org/en/latest/user-guide/usage/visualization/plot_2_cell.html), [atoms](https://docs.wulfric.org/en/latest/user-guide/usage/visualization/plot_5_atoms.html), [lattices](https://docs.wulfric.org/en/latest/user-guide/usage/visualization/plot_3_lattice.html), [k-path and k-points](https://docs.wulfric.org/en/latest/user-guide/usage/visualization/plot_6_kpath.html).

*   Common [Manipulations with cell](https://docs.wulfric.org/en/latest/user-guide/usage/cell.html) and [Manipulations with crystal](https://docs.wulfric.org/en/latest/user-guide/usage/crystal.html).


## Documentation

Extensive documentation is available at [wulfric.org](https://wulfric.org).

*   For code examples see [User guide](https://docs.wulfric.org/en/latest/user-guide/index.html).
*   For full public API see [API](https://docs.wulfric.org/en/latest/api/index.html).
*   To get some support and ask questions see [User support](https://docs.wulfric.org/en/latest/support.html).
*   To understand how transformations and rotations are performed in Wulfric; how the cells,
    atom positions, and k-points are stored see [Basic notation](https://docs.wulfric.org/en/latest/user-guide/conventions/basic-notation.html) and
    [Key concepts](https://docs.wulfric.org/en/latest/user-guide/usage/key-concepts.html).
*   To understand the difference between various cells see
    [Which cell?](https://docs.wulfric.org/en/latest/user-guide/conventions/which-cell.html).
*   To check examples of what Wulfric can visualize see
    [Visualization](https://docs.wulfric.org/en/latest/user-guide/usage/visualization/index.html).
*   For summary of releases see [Release notes](https://docs.wulfric.org/en/latest/release-notes/index.html).


## Installation

To install Wulfric, run (you may need to use ``pip3``):

```console
pip install wulfric
```

To install with visualization capabilities, run (you may need to use ``pip3``):

```console
pip install "wulfric[visual]"
```

## License

The source code of Wulfric is licensed under the  GNU General Public
License (GPL-3.0). See the ["LICENSE" file](https://github.com/adrybakov/wulfric/blob/main/LICENSE) in the [Wulfric's repository](https://github.com/adrybakov/wulfric).

In addition, if you use Wulfric in the scientific publication, cite the package as

```text
A. Rybakov, Wulfric, 2023, [software] https://github.com/adrybakov/wulfric.
```

```latex
@misc{Rybakov2023Wulfric,
  author = "Rybakov, A.",
  title  = "Wulfric",
  note   = "[software] \url{https://github.com/adrybakov/wulfric}",
  year   = "2023"}
```


For the detailed guide on how to cite the papers on which Wulfric depends
see [Citation guide](https://docs.wulfric.org/en/latest/cite.html).
