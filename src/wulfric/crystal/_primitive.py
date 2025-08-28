# ================================== LICENSE ===================================
# Wulfric - Cell, Atoms, K-path, visualization.
# Copyright (C) 2023-2025 Andrey Rybakov
#
# e-mail: anry@uv.es, web: adrybakov.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ================================ END LICENSE =================================

import numpy as np
from wulfric.crystal._crystal_validation import validate_atoms
from wulfric._exceptions import ConventionNotSupported, PotentialBugError
from wulfric._spglib_interface import get_spglib_data, validate_spglib_data
from wulfric._syntactic_sugar import SyntacticSugar
from wulfric.constants._sc_convention import SC_CONVENTIONAL_TO_PRIMITIVE
from wulfric.constants._hpkot_convention import HPKOT_CONVENTIONAL_TO_PRIMITIVE
from wulfric.crystal._conventional import get_conventional

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def _get_unique(
    prim_cell,
    non_unique_positions,
    non_unique_types,
    repetition_number,
    distance_tolerance=1e-5,
):
    r"""
    Remove equivalent atoms from the primitive cell if any.

    Parameters
    ==========
    prim_cell : (3, 3) :numpy:`ndarray`
        Matrix of the cell, Rows are interpreted as vectors. Lattice vectors of the
        primitive cell.
    non_unique_positions : (N, 3) : :numpy:`ndarray`
        Positions of the atoms of the conventional cell in the basis of ``prim_cell``.
    non_unique_types : (N, ) list of int
        Types of atoms used to distinguish between them.
    repetition_number : int
        Correct amount of repetitions of each atom type in the conventional cell.
    distance_tolerance : float, default :math:`10^{-5}`
        Tolerance parameter for comparing two linear variables.

    Returns
    =======
    prim_positions : (M, 3) : :numpy:`ndarray`
        Unique atoms of the primitive cell. ``M = N / repetition_number``.
    prim_types : (M, ) list of int
        Types of atoms in the primitive cell.
    """

    # Get closest integer
    repetition_number = int(round(repetition_number, 0))

    non_unique_types = np.array(non_unique_types, dtype=int)

    # Deal with finite precision
    # Temporary solution
    non_unique_positions = np.round(non_unique_positions, decimals=8)

    # Move all to 000
    non_unique_positions = non_unique_positions % 1

    # Done twice it fixes some problems of finite precision arithmetics
    non_unique_positions = non_unique_positions % 1

    # Compute pair-wise distances between atoms
    distances = np.linalg.norm(
        non_unique_positions[:, np.newaxis, :] - non_unique_positions[np.newaxis, :, :],
        axis=2,
    )

    # Check if two atoms are the same for each pair
    same_atoms = np.isclose(
        distances, np.zeros(distances.shape), atol=distance_tolerance
    )

    # Count amount of equivalent atoms
    n_equiv = np.sum(same_atoms, axis=1)

    # Check that each atom has correct amount of twins
    if not (n_equiv == repetition_number * np.ones(n_equiv.shape, dtype=int)).all():
        abs_pos = non_unique_positions @ prim_cell
        raise ValueError(
            f"Some atoms have wrong number of twins. Expected {repetition_number} twins for each, got\n  * "
            + "\n  * ".join(
                [
                    f"atom at {abs_pos[i][0]:.5f} {abs_pos[i][1]:.5f} {abs_pos[i][2]:.5f} "
                    + f"({non_unique_positions[i][0]:.5f} {non_unique_positions[i][1]:.5f} {non_unique_positions[i][2]:.5f} @ prim_cell) "
                    + f"with type {non_unique_types[i]} has {n_equiv} twins"
                    for i in range(len(non_unique_positions))
                ]
            )
        )

    # Find a set of unique atoms
    N = len(non_unique_positions)
    available_atoms = np.ones(N).astype(bool)
    indices = np.linspace(0, N - 1, N, dtype=int)
    unique_atoms = np.zeros(N).astype(bool)
    i = 0
    while True:
        # Do not compare with itself
        available_atoms[i] = False
        # Remove all the same atoms for the future comparisons
        for j in indices[available_atoms]:
            if same_atoms[i][j]:
                available_atoms[j] = False
        # Every index that entered in this cycle is the first encountered atom of the equivalent group.
        unique_atoms[i] = True

        # Move to the next atom, that is not accounted for yet
        if available_atoms.any():
            i = indices[available_atoms][0]
        # Or end the cycle
        else:
            break

    return non_unique_positions[unique_atoms], non_unique_types[unique_atoms]


def get_primitive(cell, atoms, convention="HPKOT", spglib_data=None):
    r"""
    Return primitive cell and atoms associated with the given ``cell`` and ``atoms``.

    Parameters
    ==========
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors.
    atoms : dict
        Dictionary with N atoms. Expected keys:

        *   "positions" : (N, 3) |array-like|_

            Positions of the atoms in the basis of lattice vectors (``cell``). In other
            words - relative coordinates of atoms.
        *   "names" : (N, ) list of str, optional

            See Notes
        *   "species" : (N, ) list of str, optional

            See Notes
        *   "spglib_types" : (N, ) list of int, optional

            See Notes

        .. hint::
            Pass ``atoms = dict(positions=[[0, 0, 0]], spglib_types=[1])`` if you would
            like to interpret the ``cell`` alone (effectively assuming that the ``cell``
            is a primitive one).

    convention : str, default "HPKOT"
        Convention for the definition of the primitive cell. Case-insensitive.
        Supported:

        * "HPKOT" for [1]_
        * "SC" for [2]_
        * "spglib" for |spglib|_

    spglib_data : :py:class:`.SyntacticSugar`, optional
        If you need more control on the parameters passed to the spglib, then
        you can get ``spglib_data`` manually and pass it to this function.
        Use wulfric's interface to |spglib|_ as

        .. code-block:: python

            spglib_data = wulfric.get_spglib_data(...)

        using the same ``cell`` and ``atoms["positions"]`` that you are passing to this
        function.

    Returns
    =======
    primitive_cell : (3, 3) :numpy:`ndarray`
        Conventional cell.
    primitive_atoms : dict
        Dictionary of atoms of the conventional cell. Has all the same keys as the
        original ``atoms``. The values of each key are updated in such a way that
        ``primitive_cell`` with ``primitive_atoms`` describe the same crystal (and
        in the same spatial orientation) as ``cell`` with ``atoms``. It has all keys as
        in ``atoms``. Additional key ``"spglib_types"`` is added if it was not present in
        ``atoms``.

    See Also
    ========
    :ref:`user-guide_conventions_which-cell`
    wulfric.crystal.get_conventional
    wulfric.get_spglib_data


    Notes
    =====
    |spglib|_ uses ``types`` to distinguish the atoms. To see how wulfric deduces the
    ``types`` for given atoms see :py:func:`wulfric.get_spglib_types`.

    If two atoms ``i`` and ``j`` have the same spglib_type (i.e.
    ``atoms["spglib_types"][i] == atoms["spglib_types"][j]``), but they have different
    property that is stored in ``atoms[key]`` (i.e ``atoms[key][i] != atoms[key][j]``),
    then those two atoms are considered equal. In the returned ``primitive_atoms``
    the value of the ``primitive_atoms[key]`` are populated base on the *last* found
    atom in ``atoms`` with each for spglib_type. This rule do not apply to the "positions"
    key.


    References
    ==========
    .. [1] Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
           Band structure diagram paths based on crystallography.
           Computational Materials Science, 128, pp.140-184.
    .. [2] Setyawan, W. and Curtarolo, S., 2010.
           High-throughput electronic band structure calculations: Challenges and tools.
           Computational materials science, 49(2), pp. 299-312.
    """

    # Validate that the atoms dictionary is what expected of it
    validate_atoms(atoms=atoms, required_keys=["positions"], raise_errors=True)

    # Call spglib
    if spglib_data is None:
        spglib_data = get_spglib_data(cell=cell, atoms=atoms)
    # Or check that spglib_data were *most likely* produced via wulfric's interface
    elif not isinstance(spglib_data, SyntacticSugar):
        raise TypeError(
            f"Are you sure that spglib_data were produced via wulfric's interface? Expected SyntacticSugar, got {type(spglib_data)}."
        )
    # Validate that user-provided spglib_data match user-provided structure
    else:
        validate_spglib_data(cell=cell, atoms=atoms, spglib_data=spglib_data)

    convention = convention.lower()

    # Straightforward interface to spglib
    if convention == "spglib":
        prim_cell = spglib_data.primitive_cell
        prim_positions = spglib_data.primitive_positions
        prim_types = spglib_data.primitive_types
    # Some work needed for other conventions
    elif convention in ["hpkot", "sc"]:
        lattice_type = spglib_data.crystal_family + spglib_data.centring_type
        conv_cell, conv_atoms = get_conventional(
            cell=cell, atoms=atoms, convention=convention, spglib_data=spglib_data
        )

        if convention == "hpkot":
            matrix = HPKOT_CONVENTIONAL_TO_PRIMITIVE[lattice_type]
        elif convention == "sc":
            matrix = SC_CONVENTIONAL_TO_PRIMITIVE[lattice_type]
        else:
            raise PotentialBugError('get_primitive(convention="HPKOT/SC").')

        prim_cell = matrix.T @ conv_cell

        non_unique_positions = (
            conv_atoms["positions"] @ conv_cell @ np.linalg.inv(prim_cell)
        )

        # Conventional cell may contain more atoms than primitive one, thus one needs to
        # remove equivalent atoms
        prim_positions, prim_types = _get_unique(
            prim_cell=prim_cell,
            non_unique_positions=non_unique_positions,
            non_unique_types=conv_atoms["spglib_types"],
            repetition_number=abs(np.linalg.det(conv_cell) / np.linalg.det(prim_cell)),
            distance_tolerance=spglib_data.symprec,
        )
    else:
        raise ConventionNotSupported(
            convention, supported_conventions=["HPKOT", "SC", "spglib"]
        )

    # Create primitive atoms
    prim_atoms = dict(positions=prim_positions)

    # Get mapping from original atoms to primitive ones through types
    types_mapping = {
        type_index: index for index, type_index in enumerate(spglib_data.original_types)
    }

    # Populate primitive_atoms with all keys that have been defined in the original atoms.
    for key in atoms:
        if key != "positions":
            prim_atoms[key] = []
            for type_index in prim_types:
                prim_atoms[key].append(atoms[key][types_mapping[type_index]])

    # Add spglib_types to new atoms if necessary
    if "spglib_types" not in prim_atoms:
        prim_atoms["spglib_types"] = prim_types

    return prim_cell, prim_atoms


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
