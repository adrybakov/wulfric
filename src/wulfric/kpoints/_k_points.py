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

from wulfric._exceptions import ConventionNotSupported
from wulfric.cell._basic_manipulation import get_reciprocal
from wulfric._spglib_interface import get_spglib_data, validate_spglib_data
from wulfric._syntactic_sugar import SyntacticSugar
from wulfric.crystal._crystal_validation import validate_atoms
from wulfric.crystal._conventional import get_conventional
from wulfric.crystal._primitive import get_primitive
from wulfric.crystal._sc_variation import sc_get_variation
from wulfric.kpoints._sc_points import _sc_get_points
from wulfric.kpoints._hpkot_points import _hpkot_get_points


# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def get_hs_points(
    cell,
    atoms,
    spglib_data=None,
    convention="HPKOT",
    relative=True,
):
    r"""
    Returns set of high symmetry points as defined in [1]_.

    Note that high symmetry points are the ones of the primitive cell, that is associated
    with the given set of ``cell`` and ``atoms``. In other words it respects the symmetry
    of the crystal.

    Parameters
    ----------
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

    spglib_data : :py:class:`.SyntacticSugar`, optional
        If you need more control on the parameters passed to the spglib, then
        you can get ``spglib_data`` manually and pass it to this function.
        Use wulfric's interface to |spglib|_ as

        .. code-block:: python

            spglib_data = wulfric.get_spglib_data(...)

        using the same ``cell`` and ``atoms["positions"]`` that you are passing to this
        function.

    convention : str, default "HPKOT"
        Convention for the definition of the conventional cell. Case-insensitive.
        Supported:

        * "HPKOT" for [1]_
        * "SC" for [2]_

    relative : bool, default True
        Whether to return coordinates as relative to the reciprocal cell or in absolute
        coordinates in the reciprocal Cartesian space.

    Returns
    -------
    hs_points : dict
        High symmetry points.

        .. code-block:: python

            hs_points = {name1: coordinate1, name2 : coordinate2, ...}

        Coordinates of the points are

        * (default) Relative to ``get_reciprocal(cell)`` if ``relative=True``.
        * Absolute in reciprocal space if ``relative=False``.

    Notes
    =====
    |spglib|_ uses ``types`` to distinguish the atoms. To see how wulfric deduces the
    ``types`` for given atoms see :py:func:`wulfric.crystal.get_spglib_types`.


    References
    ==========
    .. [1] Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
           Band structure diagram paths based on crystallography.
           Computational Materials Science, 128, pp.140-184.
    .. [2] Setyawan, W. and Curtarolo, S., 2010.
           High-throughput electronic band structure calculations: Challenges and tools.
           Computational materials science, 49(2), pp. 299-312.

    See Also
    --------
    wulfric.Kpoints : Class with a convenient interface for the same information.

    """

    cell = np.array(cell, dtype=float)

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

    conventional_cell, _ = get_conventional(
        cell=cell, atoms=atoms, convention=convention, spglib_data=spglib_data
    )
    primitive_cell, _ = get_primitive(
        cell=cell, atoms=atoms, convention=convention, spglib_data=spglib_data
    )

    lattice_type = spglib_data.crystal_family + spglib_data.centring_type

    convention = convention.lower()
    if convention == "sc":
        lattice_variation = sc_get_variation(
            cell=cell, atoms=atoms, spglib_data=spglib_data
        )
        hs_points = _sc_get_points(
            conventional_cell=conventional_cell,
            lattice_type=lattice_type,
            lattice_variation=lattice_variation,
        )
    elif convention == "hpkot":
        hs_points = _hpkot_get_points(
            conventional_cell=conventional_cell,
            lattice_type=lattice_type,
            space_group_number=spglib_data.space_group_number,
        )
        raise NotImplementedError
    else:
        raise ConventionNotSupported(convention, supported_conventions=["HPKOT", "SC"])

    primitive_rcell = get_reciprocal(cell=primitive_cell)

    for point in hs_points:
        # Here coordinates are absolute
        hs_points[point] = hs_points[point] @ primitive_rcell

        if relative:
            # absolute -> relative
            hs_points[point] = hs_points[point] @ np.linalg.inv(
                get_reciprocal(cell=cell)
            )

    return hs_points


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
