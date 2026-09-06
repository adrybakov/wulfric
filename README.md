# Wulfric

Crystal, Lattice, Atoms, K-path.


[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version](https://badge.fury.io/py/wulfric.svg)](https://badge.fury.io/py/wulfric/)
![Python](https://img.shields.io/pypi/pyversions/wulfric)

[![Documentation Status](https://readthedocs.org/projects/wulfric/badge/?version=latest)](https://wulfric.org/en/latest/?badge=latest)
[![tests (main)](https://img.shields.io/github/actions/workflow/status/adrybakov/wulfric/singular-test.yml?branch=main&label=tests%20(main))](https://github.com/adrybakov/wulfric/actions/workflows/singular-test.yml?query=branch%3Amain)
[![tests (dev)](https://img.shields.io/github/actions/workflow/status/adrybakov/wulfric/singular-test.yml?branch=dev&label=tests%20(dev))](https://github.com/adrybakov/wulfric/actions/workflows/singular-test.yml?query=branch%3Adev)


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

## Quick example

```python
import wulfric

# Create a cell
cell = [
    [5.64, 0.00, 0.00],
    [0.00, 5.64, 0.00],
    [0.00, 0.00, 5.64],
]

# Create atoms
atoms = {
    "names" : ["Cl1", "Cl2", "Cl3", "Cl4", "Na1", "Na2", "Na3", "Na4"],
    "positions" : [
        [0.0, 0.0, 0.0], # Cl1
        [0.5, 0.5, 0.0], # Cl2
        [0.5, 0.0, 0.5], # Cl3
        [0.0, 0.5, 0.5], # Cl4
        [0.5, 0.5, 0.5], # Na1
        [0.5, 0.0, 0.0], # Na2
        [0.0, 0.5, 0.0], # Na3
        [0.0, 0.0, 0.5], # Na4
    ]
}

# (Optional) Call spglib once, to prevent other functions calling it every time
spglib_data = wulfric.get_spglib_data(cell, atoms)
```

### Primitive cell

```python
# Primitive cell, using default convention (HPKOT)
prim_cell, prim_atoms = wulfric.crystal.get_primitive(
    cell=cell,
    atoms=atoms,
    spglib_data=spglib_data, # Optional
)

print(prim_cell)
print(prim_atoms["names"])
```

### Conventional cell

```python
# Conventional cell, using default convention (HPKOT)
conv_cell, conv_atoms = wulfric.crystal.get_conventional(
    cell=cell,
    atoms=atoms,
    spglib_data=spglib_data, # Optional
)

print(conv_cell)
print(conv_atoms["names"])
```

### K-points and K-path choice
```python
# In SC convention
kp_SC = wulfric.Kpoints.from_crystal(
    cell=cell,
    atoms=atoms,
    convention="SC",
    spglib_data=spglib_data, # Optional
)

kp_HPKOT = wulfric.Kpoints.from_crystal(
    cell=cell,
    atoms=atoms,
    convention="HPKOT",
    spglib_data=spglib_data, # Optional
)

print(f"K-path (SC): {kp_SC.path}")
print(f"K-path (HPKOT): {kp_HPKOT.path}")
```

### Compute dispersion or band structure

Or any k-resolved data

```python
# Pick convention
kp = kp_HPKOT

# Customize k-path
...

# Set amount of intermediate point for each section of the k-path
kp.n = 50

# Compute point-by-point
bands = []
for point in kp.points(relative=False):
    bands.append(
        # Your data/routine
        compute_single_point(kpoint=point, ...)
    )



# Or all at once
bands = compute_all_points(
    # Your data/routine
    kpoints=kp.points(relative=False) 
)
```


### Plotting dispersion or band structure
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

# Assume that bands[i] is a single band
for band in bands:
    # Automatically convert list of k-points into a flat index
    plot(kp.flat_points(relative=False), band) 

# Automatic xlabels at high-symmetry points
ax.set_xticks(kp.ticks(relative=False), kp.labels)

# Automatic vlines at high-symmetry points
ax.vlines(
    kp.ticks(relative=False),
    0,
    1,
    color="grey",
    lw=0.5,
    transform=ax.get_xaxis_transform(),
)

# Automatic correct xlimits
ax.set_xlim(kp.ticks(relative=False)[0], kp.ticks(relative=False)[-1])

fig.savefig("plot.png", dpi=400, bbox_inches="tight")
plt.close()
```


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
