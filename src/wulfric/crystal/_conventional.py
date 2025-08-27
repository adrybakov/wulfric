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

from wulfric._exceptions import ConventionNotSupported, PotentialBugError
from wulfric.crystal._crystal_validation import validate_atoms
from wulfric.cell._niggli import get_niggli
from wulfric.cell._basic_manipulation import get_reciprocal, get_params
from wulfric._spglib_interface import get_spglib_data, validate_spglib_data
from wulfric._syntactic_sugar import SyntacticSugar

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def _hpkot_get_conventional_a(spglib_std_lattice):
    r"""
    Special case of hkpot convention and aP lattice

    Parameters
    ==========
    spglib_std_lattice : (3, 3) :numpy:`ndarray`
        Conventional cell found by spglib.

    Returns
    =======
    conv_cell : (3, 3) :numpy:`ndarray`
        Conventional cell as per the convention of HPKOT.
    """

    # Step 1 - get cell that is niggli-reduced in reciprocal space
    r_cell_step_1 = get_niggli(cell=get_reciprocal(spglib_std_lattice))
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
        raise PotentialBugError(
            '(convention="HPKOT"): aP lattice, step 2. Values of the dot products fall outside of three cases, which should be impossible.'
        )

    cell_step_2 = matrix_to_2.T @ cell_step_1

    # Step 3
    _, _, _, r_alpha, r_beta, r_gamma = get_params(
        cell=get_reciprocal(cell=cell_step_2)
    )

    if (r_alpha < 90.0 and r_beta < 90.0 and r_gamma < 90.0) or (
        r_alpha >= 90.0 and r_beta >= 90.0 and r_gamma >= 90.0
    ):
        matrix_to_3 = np.eye(3, dtype=float)
    elif (r_alpha > 90.0 and r_beta > 90.0 and r_gamma < 90.0) or (
        r_alpha <= 90.0 and r_beta <= 90.0 and r_gamma >= 90.0
    ):
        matrix_to_3 = np.array(
            [
                [-1, 0, 0],
                [0, -1, 0],
                [0, 0, 1],
            ],
            dtype=float,
        )
    elif (r_alpha > 90.0 and r_beta < 90.0 and r_gamma > 90.0) or (
        r_alpha <= 90.0 and r_beta >= 90.0 and r_gamma <= 90.0
    ):
        matrix_to_3 = np.array(
            [
                [-1, 0, 0],
                [0, 1, 0],
                [0, 0, -1],
            ],
            dtype=float,
        )
    elif (r_alpha < 90.0 and r_beta > 90.0 and r_gamma > 90.0) or (
        r_alpha >= 90.0 and r_beta <= 90.0 and r_gamma <= 90.0
    ):
        matrix_to_3 = np.array(
            [
                [1, 0, 0],
                [0, -1, 0],
                [0, 0, -1],
            ],
            dtype=float,
        )
    else:
        raise PotentialBugError(
            '(convention="HPKOT"): aP lattice, step 3. Values of the reciprocal angles  fall outside of four cases, which should be impossible.'
        )

    return matrix_to_3.T @ cell_step_2


def _sc_get_conventional_oPFI(spglib_std_lattice):
    r"""
    Case of SC convention and oP, oF or oI lattice.

    Choose the cell with the lattice parameters that satisfy

    * ``a < b < c``
    * ``alpha = beta = gamma = 90``

    Parameters
    ==========
    spglib_std_lattice : (3, 3) :numpy:`ndarray`
        Conventional cell found by spglib.

    Returns
    =======
    conv_cell : (3, 3) :numpy:`ndarray`
        Conventional cell as per the convention of SC.
    """

    a, b, c, _, _, _ = get_params(cell=spglib_std_lattice)

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
        raise PotentialBugError(
            '(convention="SC"): oP, oF, oI lattices. Length of the lattice vectors fall outside of six cases, which should be impossible.'
        )

    return matrix.T @ spglib_std_lattice


def _sc_get_conventional_oC(spglib_std_lattice):
    r"""
    Case of SC convention and oC lattice.

    Choose the cell with the lattice parameters that satisfy

    * ``a < b``
    * ``alpha = beta = gamma = 90``

    Parameters
    ==========
    spglib_std_lattice : (3, 3) :numpy:`ndarray`
        Conventional cell found by spglib.

    Returns
    =======
    conv_cell : (3, 3) :numpy:`ndarray`
        Conventional cell as per the convention of SC.
    """

    a, b, _, _, _, _ = get_params(cell=spglib_std_lattice)

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
        raise PotentialBugError(
            '(convention="SC"): oC lattices. Length of the lattice vectors fall outside of six cases, which should be impossible.'
        )

    return matrix.T @ spglib_std_lattice


def _sc_get_conventional_m(spglib_std_lattice):
    r"""
    Case of SC convention and m lattice.

    Choose the cell with the lattice parameters that satisfy

    * ``b <= c``
    * ``alpha < 90``

    Parameters
    ==========
    spglib_std_lattice : (3, 3) :numpy:`ndarray`
        Conventional cell found by spglib.

    Returns
    =======
    conv_cell : (3, 3) :numpy:`ndarray`
        Conventional cell as per the convention of SC.
    """

    # Step 1, make sure that alpha is not a 90 angle
    _, _, _, alpha, beta, gamma = get_params(cell=spglib_std_lattice)
    if beta == 90.0 and gamma == 90.0:  # No change
        matrix_to_1 = np.eye(3, dtype=float)
    elif alpha == 90.0 and beta == 90.0:  # -> a3, a1, a2
        matrix_to_1 = np.array(
            [
                [0, 1, 0],
                [0, 0, 1],
                [1, 0, 0],
            ]
        )
    elif alpha == 90.0 and gamma == 90.0:  # -> a2, a3, a1
        matrix_to_1 = np.array(
            [
                [0, 0, 1],
                [1, 0, 0],
                [0, 1, 0],
            ]
        )
    else:
        raise PotentialBugError(
            '(convention="SC"): m lattice, step 1. Angles fall out of the three cases.'
        )
    cell_step_1 = matrix_to_1.T @ spglib_std_lattice

    # Step 2, make sure that b <= c
    _, b, c, _, _, _ = get_params(cell=cell_step_1)
    if b <= c:
        matrix_to_2 = np.eye(3, dtype=float)
    else:  # -> -a1, a3, a2
        matrix_to_2 = np.array(
            [
                [-1, 0, 0],
                [0, 0, 1],
                [0, 1, 0],
            ],
            dtype=float,
        )
    cell_step_2 = matrix_to_2.T @ cell_step_1

    # Step 3, make sure that alpha < 90
    _, _, _, alpha, _, _ = get_params(cell=cell_step_2)
    if alpha <= 90.0:  # No change
        matrix_to_3 = np.eye(3, dtype=float)
    else:  # -> -a1, -a2, a3
        matrix_to_3 = np.array(
            [
                [-1, 0, 0],
                [0, -1, 0],
                [0, 0, 1],
            ]
        )

    return matrix_to_3.T @ cell_step_2


def _sc_get_conventional_a(spglib_std_lattice):
    r"""
    Case of SC convention and a lattice.

    Choose the cell with the lattice parameters that satisfy

    * ``b <= c``
    * ``alpha < 90``

    Parameters
    ==========
    spglib_std_lattice : (3, 3) :numpy:`ndarray`
        Conventional cell found by spglib.

    Returns
    =======
    conv_cell : (3, 3) :numpy:`ndarray`
        Conventional cell as per the convention of SC.
    """

    # Compute reciprocal cell
    r_cell = get_reciprocal(cell=spglib_std_lattice)

    # Step 1
    _, _, _, r_alpha, r_beta, r_gamma = get_params(cell=r_cell)

    if (r_alpha < 90.0 and r_beta < 90.0 and r_gamma < 90.0) or (
        r_alpha >= 90.0 and r_beta >= 90.0 and r_gamma >= 90.0
    ):
        matrix_to_1 = np.eye(3, dtype=float)
    elif (r_alpha > 90.0 and r_beta > 90.0 and r_gamma < 90.0) or (
        r_alpha <= 90.0 and r_beta <= 90.0 and r_gamma >= 90.0
    ):
        matrix_to_1 = np.array(
            [
                [-1, 0, 0],
                [0, -1, 0],
                [0, 0, 1],
            ],
            dtype=float,
        )
    elif (r_alpha > 90.0 and r_beta < 90.0 and r_gamma > 90.0) or (
        r_alpha <= 90.0 and r_beta >= 90.0 and r_gamma <= 90.0
    ):
        matrix_to_1 = np.array(
            [
                [-1, 0, 0],
                [0, 1, 0],
                [0, 0, -1],
            ],
            dtype=float,
        )
    elif (r_alpha < 90.0 and r_beta > 90.0 and r_gamma > 90.0) or (
        r_alpha >= 90.0 and r_beta <= 90.0 and r_gamma <= 90.0
    ):
        matrix_to_1 = np.array(
            [
                [1, 0, 0],
                [0, -1, 0],
                [0, 0, -1],
            ],
            dtype=float,
        )
    else:
        raise PotentialBugError(
            '(convention="SC"): aP lattice, step 1. Values of the reciprocal angles fall outside of four cases, which should be impossible.'
        )
    r_cell_step_1 = matrix_to_1.T @ r_cell

    # Step 2
    # Note np.linalg.inv(matrix_to_1) == matrix_to_1.T
    _, _, _, r_alpha, r_beta, r_gamma = get_params(cell=r_cell_step_1)

    if (
        r_gamma == min(r_alpha, r_beta, r_gamma)
        and r_gamma >= 90.0
        or (r_gamma == max(r_alpha, r_beta, r_gamma) and r_gamma <= 90.0)
    ):
        matrix_to_2 = np.eye(3, dtype=float)
    elif (
        r_beta == min(r_alpha, r_beta, r_gamma)
        and r_beta >= 90.0
        or (r_beta == max(r_alpha, r_beta, r_gamma) and r_beta <= 90.0)
    ):
        matrix_to_2 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    elif (
        r_alpha == min(r_alpha, r_beta, r_gamma)
        and r_alpha >= 90.0
        or (r_alpha == max(r_alpha, r_beta, r_gamma) and r_alpha <= 90.0)
    ):
        matrix_to_2 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    else:
        raise PotentialBugError(
            '(convention="SC"): aP lattice, step 2. Values of the reciprocal angles fall outside of four cases, which should be impossible.'
        )

    return matrix_to_2.T @ get_reciprocal(cell=r_cell_step_1)


def _sc_get_conventional_hR(spglib_primitive_cell):
    r"""
    Computes conventional cell for the case of SC and hR lattice.

    It checks that

    * All three angles between the lattice vectors are equal

    * All lattice vectors have the same length

    Parameters
    ==========
    spglib_primitive_cell : (3, 3) :numpy:`ndarray`
        Primitive cell found by spglib.

    Returns
    =======
    conv_cell : (3, 3) :numpy:`ndarray`
        Conventional cell as per the convention of SC.
    """

    a, b, c, alpha, beta, gamma = get_params(cell=spglib_primitive_cell)

    if abs(a - b) > 1e-5 or abs(a - c) > 1e-5 or abs(b - c) > 1e-5:
        raise PotentialBugError(
            f'(convention="SC"): hR lattice. Lattice vectors have different lengths with the precision of {1e-5:.5e}'
        )

    if alpha == beta == gamma:
        matrix = np.eye(3, dtype=float)
    elif 180 - alpha == beta == gamma:  # -> a1, -a2, -a3
        matrix = np.array(
            [
                [1, 0, 0],
                [0, -1, 0],
                [0, 0, -1],
            ]
        )
    elif alpha == 180 - beta == gamma:  # -> -a1, a2, -a3
        matrix = np.array(
            [
                [-1, 0, 0],
                [0, 1, 0],
                [0, 0, -1],
            ]
        )
    elif alpha == beta == 180 - gamma:  # -> -a1, -a2, a3
        matrix = np.array(
            [
                [-1, 0, 0],
                [0, -1, 0],
                [0, 0, 1],
            ]
        )
    else:
        raise PotentialBugError(
            '(convention="SC"): hR lattice. Angles can not be made equal.'
        )

    return matrix.T @ spglib_primitive_cell


def _sc_get_conventional_no_hR(spglib_std_lattice, crystal_family, centring_type):
    r"""
    Computes conventional lattice for the case of SC.

    Note: do not process hR, as it is treated separately.

    Parameters
    ==========
    spglib_std_lattice : (3, 3) :numpy:`ndarray`
        Conventional cell found by spglib.
    crystal_family : str
    centring_type : str

    Returns
    =======
    conv_cell : (3, 3) :numpy:`ndarray`
        Conventional cell as per the convention of SC.
    """
    # Run over possible crystal families but hR
    if crystal_family in ["c", "t"] or (crystal_family == "h" and centring_type == "P"):
        conv_cell = spglib_std_lattice
    elif crystal_family == "o":
        if centring_type in ["P", "F", "I"]:
            conv_cell = _sc_get_conventional_oPFI(spglib_std_lattice=spglib_std_lattice)
        elif centring_type == "C":
            conv_cell = _sc_get_conventional_oC(spglib_std_lattice=spglib_std_lattice)
        elif centring_type == "A":
            # Make it C-centered
            # a1, a2, a3 -> a2, a3, a1
            # and treat like one
            matrix = np.array(
                [
                    [0, 0, 1],
                    [1, 0, 0],
                    [0, 1, 0],
                ]
            )
            conv_cell = _sc_get_conventional_oC(spglib_std_lattice=matrix.T @ conv_cell)
        else:
            raise PotentialBugError(
                f'(convention="sc"): crystal family "o". Unexpected centring type "{centring_type}", which should be impossible.'
            )
    elif crystal_family == "m":
        conv_cell = _sc_get_conventional_m(spglib_std_lattice=spglib_std_lattice)
    elif crystal_family == "a":
        conv_cell = _sc_get_conventional_a(spglib_std_lattice=spglib_std_lattice)
    else:
        raise PotentialBugError(
            f'(convention="sc"): unexpected crystal family "{crystal_family}", which should be impossible.'
        )

    return conv_cell


def get_conventional(cell, atoms, convention="HPKOT", spglib_data=None):
    r"""
    Return conventional cell and atoms associated with the given ``cell`` and ``atoms``.

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
        Convention for the definition of the conventional cell. Case-insensitive.
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
    conventional_cell : (3, 3) :numpy:`ndarray`
        Conventional cell.
    conventional_atoms : dict
        Dictionary of atoms of the conventional cell. Has all the same keys as the
        original ``atoms``. The values of each key are updated in such a way that
        ``conventional_cell`` with ``conventional_atoms`` describe the same crystal (and
        in the same spatial orientation) as ``cell`` with ``atoms``. It has all keys as
        in ``atoms``. Additional key ``"spglib_types"`` is added if it was not present in
        ``atoms``.

    See Also
    ========
    :ref:`user-guide_conventions_which-cell`
    wulfric.crystal.get_primitive
    wulfric.get_spglib_data


    Notes
    =====
    |spglib|_ uses ``types`` to distinguish the atoms. To see how wulfric deduces the
    ``types`` for given atoms see :py:func:`wulfric.get_spglib_types`.

    If two atoms ``i`` and ``j`` have the same spglib_type (i.e.
    ``atoms["spglib_types"][i] == atoms["spglib_types"][j]``), but they have different
    property that is stored in ``atoms[key]`` (i.e ``atoms[key][i] != atoms[key][j]``),
    then those two atoms are considered equal. In the returned ``conventional_atoms``
    the value of the ``conventional_atoms[key]`` are populated based on the *last* found
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

    # Define conventional cell, positions and types
    convention = convention.lower()
    if convention == "spglib" or convention == "hpkot":
        if convention == "hpkot" and spglib_data.crystal_family == "a":
            # Find a conventional cell and update atom positions
            conv_cell = _hpkot_get_conventional_a(
                spglib_std_lattice=spglib_data.conventional_cell
            )
            # Compute relative positions with respect to the new cell
            # relative spglib -> Cartesian -> relative HPKOT
            conv_positions = (
                spglib_data.conventional_positions
                @ spglib_data.conventional_cell
                @ np.linalg.inv(conv_cell)
            )
        else:
            conv_cell = spglib_data.conventional_cell
            conv_positions = spglib_data.conventional_positions

        conv_types = spglib_data.conventional_types

    elif convention == "sc":
        # Treat hR in a special way, as it changes the volume of the cell
        if spglib_data.crystal_family == "h" and spglib_data.centring_type == "R":
            # Fix potential convention mismatch
            conv_cell = _sc_get_conventional_hR(
                spglib_primitive_cell=spglib_data.primitive_cell
            )

            # Update positions
            # relative spglib -> Cartesian -> relative SC
            conv_positions = (
                spglib_data.primitive_positions
                @ spglib_data.primitive_cell
                @ np.linalg.inv(conv_cell)
            )
            conv_types = spglib_data.primitive_types

        # The rest do not change the volume of the cell
        else:
            conv_cell = _sc_get_conventional_no_hR(
                spglib_std_lattice=spglib_data.conventional_cell,
                crystal_family=spglib_data.crystal_family,
                centring_type=spglib_data.centring_type,
            )
            # relative spglib -> Cartesian -> relative SC
            conv_positions = (
                spglib_data.conventional_positions
                @ spglib_data.conventional_cell
                @ np.linalg.inv(conv_cell)
            )
            conv_types = spglib_data.conventional_types

    else:
        raise ConventionNotSupported(
            convention, supported_conventions=["HPKOT", "SC", "spglib"]
        )

    # Create conventional atoms
    conv_atoms = dict(positions=conv_positions)

    # Get mapping from original atoms to conventional ones through types
    types_mapping = {
        type_index: index for index, type_index in enumerate(spglib_data.original_types)
    }

    # Populate conv_atoms with all keys that have been defined in the original atoms.
    for key in atoms:
        if key != "positions":
            conv_atoms[key] = []
            for type_index in conv_types:
                conv_atoms[key].append(atoms[key][types_mapping[type_index]])

    # Add spglib_types to new atoms if necessary
    if "spglib_types" not in conv_atoms:
        conv_atoms["spglib_types"] = conv_types

    return conv_cell, conv_atoms


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
