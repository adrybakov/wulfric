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
import spglib
import numpy as np

from wulfric.constants._space_groups import CRYSTAL_FAMILY, CENTRING_TYPE
from wulfric._exceptions import ConventionNotSupported, UnexpectedError
from wulfric.crystal._crystal_validation import validate_atoms
from wulfric.crystal._atoms import get_spglib_types
from wulfric.crystal._basic_manipulation import get_spatial_mapping
from wulfric.cell._niggli import get_niggli
from wulfric.cell._basic_manipulation import get_reciprocal, get_params

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def _hpkot_get_conventional_aP(spglib_conv_cell, spglib_conv_positions):
    r"""
    Special case of hkpot convention and aP lattice

    Parameters
    ==========
    spglib_conv_cell : (3, 3) :numpy:`ndarray`
        Conventional cell found by spglib.
    spglib_conv_positions : (N, 3) :numpy:`ndarray`
        Relative positions of the atoms in the basis of the ``spglib_conv_cell``.

    Returns
    =======
    conv_cell : (3, 3) :numpy:`ndarray`
        Conventional cell as per the convention of HPKOT.
    conv_positions : (N, 3) :numpy:`ndarray`
        Relative positions of the atoms in the basis of the new ``conv_cell``.
    """

    # Step 1 - get cell that is niggli-reduced in reciprocal space
    r_cell_step_1 = get_niggli(cell=get_reciprocal(spglib_conv_cell))
    cell_step_1 = get_reciprocal(r_cell_step_1)

    # Step 2
    dot_bc = abs(r_cell_step_1[1] @ r_cell_step_1[2])
    dot_ac = abs(r_cell_step_1[0] @ r_cell_step_1[2])
    dot_ab = abs(r_cell_step_1[0] @ r_cell_step_1[1])

    if dot_bc <= dot_ac and dot_bc <= dot_ab:
        matrix_to_2 = np.array(
            [
                [0, 0, 1],
                [1, 0, 0],
                [0, 1, 0],
            ]
        )
    elif dot_ac <= dot_bc and dot_ac <= dot_ab:
        matrix_to_2 = np.array(
            [
                [0, 1, 0],
                [0, 0, 1],
                [1, 0, 0],
            ]
        )
    elif dot_ab <= dot_ac and dot_ab <= dot_bc:
        matrix_to_2 = np.eye(3, dtype=float)
    else:
        raise UnexpectedError(
            '(convention="HPKOT"): aP lattice, step 2. Values of the dot products fall '
            "outside of three cases, which should be impossible."
        )

    cell_step_2 = matrix_to_2.T @ cell_step_1

    # Step 3
    _, _, _, r_alpha, r_beta, r_gamma = get_params(
        cell=get_reciprocal(cell=cell_step_2)
    )

    if (r_alpha < 90 and r_beta < 90 and r_gamma < 90) or (
        r_alpha >= 90 and r_beta >= 90 and r_gamma >= 90
    ):
        matrix_to_3 = np.eye(3, dtype=float)
    elif (r_alpha < 90 and r_beta > 90 and r_gamma > 90) or (
        r_alpha >= 90 and r_beta <= 90 and r_gamma <= 90
    ):
        matrix_to_3 = np.array(
            [
                [1, 0, 0],
                [0, -1, 0],
                [0, 0, -1],
            ]
        )

    elif (r_alpha > 90 and r_beta < 90 and r_gamma > 90) or (
        r_alpha <= 90 and r_beta >= 90 and r_gamma <= 90
    ):
        matrix_to_3 = np.array(
            [
                [-1, 0, 0],
                [0, 1, 0],
                [0, 0, -1],
            ]
        )

    elif (r_alpha > 90 and r_beta > 90 and r_gamma < 90) or (
        r_alpha <= 90 and r_beta <= 90 and r_gamma >= 90
    ):
        matrix_to_3 = np.array(
            [
                [-1, 0, 0],
                [0, -1, 0],
                [0, 0, 1],
            ]
        )
    else:
        raise UnexpectedError(
            '(convention="HPKOT"): aP lattice, step 3. Values of the reciprocal angles '
            "fall outside of four cases, which should be impossible."
        )

    cell_step_3 = matrix_to_3.T @ cell_step_2

    conv_cell = cell_step_3
    # relative spglib -> cartesian -> relative HPKOT
    conv_positions = spglib_conv_positions @ spglib_conv_cell @ np.linalg.inv(conv_cell)

    return conv_cell, conv_positions


def _sc_get_conventional_oPFI(spglib_conv_cell, spglib_conv_positions):
    r"""
    Case of SC convention and oP, oF or oI lattice.

    Choose the cell with the lattice parameters that satisfy

    * ``a < b < c``
    * ``alpha = beta = gamma = 90``

    Parameters
    ==========
    spglib_conv_cell : (3, 3) :numpy:`ndarray`
        Conventional cell found by spglib.
    spglib_conv_positions : (N, 3) :numpy:`ndarray`
        Relative positions of the atoms in the basis of the ``spglib_conv_cell``.

    Returns
    =======
    conv_cell : (3, 3) :numpy:`ndarray`
        Conventional cell as per the convention of SC.
    conv_positions : (N, 3) :numpy:`ndarray`
        Relative positions of the atoms in the basis of the new ``conv_cell``.
    """

    a, b, c, _, _, _ = get_params(cell=spglib_conv_cell)

    if a < b < c:  # No change
        matrix = np.eye(3, dtype=float)
    elif a < c < b:  # -> -a1, -a3, -a2
        matrix = np.array(
            [
                [-1, 0, 0],
                [0, 0, -1],
                [0, -1, 0],
            ],
            dtype=float,
        )
    elif b < a < c:  # -> -a2, -a1, -a3
        matrix = np.array(
            [
                [0, -1, 0],
                [-1, 0, 0],
                [0, 0, -1],
            ],
            dtype=float,
        )
    elif b < c < a:  # -> a2, a3, a1
        matrix = np.array(
            [
                [0, 0, 1],
                [1, 0, 0],
                [0, 1, 0],
            ],
            dtype=float,
        )
    elif c < a < b:  # -> a3, a1, a2
        matrix = np.array(
            [
                [0, 1, 0],
                [0, 0, 1],
                [1, 0, 0],
            ],
            dtype=float,
        )
    elif c < b < a:  # -> -a3, -a2, -a1
        matrix = np.array(
            [
                [0, 0, -1],
                [0, -1, 0],
                [-1, 0, 0],
            ],
            dtype=float,
        )
    else:
        raise UnexpectedError(
            '(convention="SC"): oP, oF, oI lattices. Length of the lattice vectors fall '
            "outside of six cases, which should be impossible."
        )

    conv_cell = matrix.T @ spglib_conv_cell
    # relative spglib -> cartesian -> relative SC
    conv_positions = spglib_conv_positions @ spglib_conv_cell @ np.linalg.inv(conv_cell)

    return conv_cell, conv_positions


def _sc_get_conventional_oC(spglib_conv_cell, spglib_conv_positions):
    r"""
    Case of SC convention and oC lattice.

    Choose the cell with the lattice parameters that satisfy

    * ``a < b``
    * ``alpha = beta = gamma = 90``

    Parameters
    ==========
    spglib_conv_cell : (3, 3) :numpy:`ndarray`
        Conventional cell found by spglib.
    spglib_conv_positions : (N, 3) :numpy:`ndarray`
        Relative positions of the atoms in the basis of the ``spglib_conv_cell``.

    Returns
    =======
    conv_cell : (3, 3) :numpy:`ndarray`
        Conventional cell as per the convention of SC.
    conv_positions : (N, 3) :numpy:`ndarray`
        Relative positions of the atoms in the basis of the new ``conv_cell``.
    """

    a, b, _, _, _, _ = get_params(cell=spglib_conv_cell)

    if a < b:  # No change
        matrix = np.eye(3, dtype=float)
    elif b < a:  # -> a2, -a1, a3
        matrix = np.array(
            [
                [0, -1, 0],
                [1, 0, 0],
                [0, 0, 1],
            ],
            dtype=float,
        )
    else:
        raise UnexpectedError(
            '(convention="SC"): oC lattices. Length of the lattice vectors fall '
            "outside of six cases, which should be impossible."
        )

    conv_cell = matrix.T @ spglib_conv_cell
    # relative spglib -> cartesian -> relative SC
    conv_positions = spglib_conv_positions @ spglib_conv_cell @ np.linalg.inv(conv_cell)

    return conv_cell, conv_positions


def get_conventional(
    cell,
    atoms,
    convention="HPKOT",
    spglib_symprec=1e-5,
    spglib_angle_tolerance=-1,
):
    r"""
    Return conventional cell associated with the given ``cell``.

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
        *   "spglib_types" (N, ) list of int, optional
            See Notes

        .. hint::
            Pass ``atoms = dict(positions=[[0, 0, 0]], spglib_types=[1])`` if you would
            like to interpret the ``cell`` alone (effectively assuming that the ``cell``
            is a primitive one).

    convention : str, default "HPKOT"
        Convention for the definition of the conventional cell. Case-insensitive.
        Supported:

        * "HPKOT" for [1]_
        * "SC" for [2]_
        * "spglib" for |spglib|_

    spglib_symprec : float, default 1e-5
        Tolerance parameter for the symmetry search, that is passed to |spglib|_. Quote
        from its documentation: "Symmetry search tolerance in the unit of length".
    spglib_angle_tolerance : float, default -1
        Tolerance parameter for the symmetry search, that is passed to |spglib|_. Quote
        from its documentation: "Symmetry search tolerance in the unit of angle deg.
        Normally it is not recommended to use this argument. If the value is
        negative, an internally optimized routine is used to judge symmetry.

    Returns
    =======
    conventional_cell : (3, 3) :numpy:`ndarray`
        Conventional cell.
    conventional_atoms : dict
        Dictionary of atoms of the conventional cell. Has all the same keys as the
        original ``atoms``. The values of each key are updated in such a way that
        ``conventional_cell`` with ``conventional_atoms`` describe the same crystal (and
        in the same spatial orientation) as ``cell`` with ``atoms``.

    See Also
    ========
    :ref:`user-guide_conventions_which-cell`
    wulfric.crystal.get_primitive


    Notes
    =====
    |spglib|_ uses ``types`` to distinguish the atoms. To see how wulfric deduces the
    ``types`` see :ref:`wulfric.crystal.get_spglib_types()`.


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

    dataset = spglib.get_symmetry_dataset(
        (cell, atoms["positions"], get_spglib_types(atoms=atoms)),
        symprec=spglib_symprec,
        angle_tolerance=spglib_angle_tolerance,
    )

    spglib_conv_cell = dataset.std_lattice @ dataset.std_rotation_matrix
    spglib_conv_positions = dataset.std_positions
    crystal_family = CRYSTAL_FAMILY[dataset.number]
    centring_type = CENTRING_TYPE[dataset.number]

    convention = convention.lower()
    if convention == "spglib" or convention == "hpkot":
        # Note:
        # dataset.std_types might not distinguish between atoms with different properties
        # of some atoms[key].
        # Therefore, wulfric needs to match the cartesian coordinates of the atoms
        # of the conventional lattice with the cartesian coordinates of the atoms
        # of the original original lattice.
        # Even in the case when the results of spglib are returned straight away.

        if convention == "hpkot" and crystal_family == "a":
            # Find a conventional cell and update atom positions
            conv_cell, conv_positions = _hpkot_get_conventional_aP(
                spglib_conv_cell=spglib_conv_cell,
                spglib_conv_positions=spglib_conv_positions,
            )
        else:
            conv_cell = spglib_conv_cell
            conv_positions = spglib_conv_positions

    elif convention == "sc":
        # Run over possible crystal families
        if crystal_family in ["c", "t"] or (
            crystal_family == "h" and centring_type == "P"
        ):
            conv_cell = spglib_conv_cell
            conv_positions = spglib_conv_positions
        elif crystal_family == "h" and centring_type == "R":
            raise NotImplementedError
        elif crystal_family == "o":
            if centring_type in ["P", "F", "I"]:
                conv_cell, conv_positions = _sc_get_conventional_oPFI(
                    spglib_conv_cell=spglib_conv_cell,
                    spglib_conv_positions=spglib_conv_positions,
                )
            elif centring_type == "C":
                conv_cell, conv_positions = _sc_get_conventional_oC(
                    spglib_conv_cell=spglib_conv_cell,
                    spglib_conv_positions=spglib_conv_positions,
                )
            elif centring_type == "A":
                # Make it C-centered
                # a1, a2, a3 -> a2, a3, a1
                matrix = np.array(
                    [
                        [0, 0, 1],
                        [1, 0, 0],
                        [0, 1, 0],
                    ]
                )
                # Transform cell
                spglib_conv_cell = matrix.T @ spglib_conv_cell
                # Transform positions
                # Note that np.linalg.inv(matrix) == matrix.T
                spglib_conv_positions = spglib_conv_positions @ matrix

                # And treat like one
                conv_cell, conv_positions = _sc_get_conventional_oC(
                    spglib_conv_cell=spglib_conv_cell,
                    spglib_conv_positions=spglib_conv_positions,
                )
            else:
                raise UnexpectedError(
                    '(convention="sc"): crystal family "o". Unexpected centring type '
                    f'"{centring_type}", which should be impossible.'
                )
        elif crystal_family == "m":
            raise NotImplementedError
        elif crystal_family == "a":
            raise NotImplementedError
        else:
            raise UnexpectedError(
                f'(convention="sc"): unexpected crystal family "{crystal_family}", '
                "which should be impossible."
            )

    else:
        raise ConventionNotSupported(convention, with_spglib=True)

    conv_atoms = dict(positions=conv_positions)

    # Get the mapping from the original atoms
    #   len(mapping) == len(new_positions)
    #   mapping[i] is an index of old_positions
    mapping = get_spatial_mapping(
        old_cell=cell,
        old_positions=atoms["positions"],
        new_cell=spglib_conv_cell,
        new_positions=spglib_conv_positions,
    )

    # Populate conv_atoms with all keys that have been defined in the original atoms.
    for key in atoms:
        if key != "positions":
            conv_atoms[key] = []
            for index in mapping:
                conv_atoms[key].append(atoms[key][index])

    return conv_cell, conv_atoms


def get_primitive(
    cell,
    atoms,
    convention="HPKOT",
    spglib_symprec=1e-5,
    spglib_angle_tolerance=-1,
):
    r"""
    Return primitive cell cell associated with the given ``cell``.

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
        *   "spglib_types" (N, ) list of int, optional
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

    spglib_symprec : float, default 1e-5
        Tolerance parameter for the symmetry search, that is passed to |spglib|_. Quote
        from its documentation: "Symmetry search tolerance in the unit of length".
    spglib_angle_tolerance : float, default -1
        Tolerance parameter for the symmetry search, that is passed to |spglib|_. Quote
        from its documentation: "Symmetry search tolerance in the unit of angle deg.
        Normally it is not recommended to use this argument. If the value is
        negative, an internally optimized routine is used to judge symmetry.

    Returns
    =======
    primitive_cell : (3, 3) :numpy:`ndarray`
        Primitive cell.
    primitive_atoms : dict
        Dictionary of atoms of the primitive cell. Has all the same keys as the
        original ``atoms``. The values of each key are updated in such a way that
        ``primitive_cell`` with ``primitive_atoms`` describe the same crystal (and
        in the same spatial orientation) as ``cell`` with ``atoms``.

    See Also
    ========
    :ref:`user-guide_conventions_which-cell`
    wulfric.crystal.get_conventional

    Notes
    =====
    |spglib|_ uses ``types`` to distinguish the atoms. To see how wulfric deduces the
    ``types`` see :ref:`wulfric.crystal.get_spglib_types()`.


    References
    ==========
    .. [1] Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
           Band structure diagram paths based on crystallography.
           Computational Materials Science, 128, pp.140-184.
    .. [2] Setyawan, W. and Curtarolo, S., 2010.
           High-throughput electronic band structure calculations: Challenges and tools.
           Computational materials science, 49(2), pp. 299-312.
    """


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
