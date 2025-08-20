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

from wulfric.crystal._crystal_validation import validate_atoms, validate_spglib_data
from wulfric._exceptions import ConventionNotSupported
from wulfric._spglib_interface import get_spglib_data
from wulfric._syntactic_sugar import SyntacticSugar

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


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
    ``types`` for given atoms see :py:func:`wulfric.crystal.get_spglib_types`.

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

    # Call for spglib
    if spglib_data is None:
        spglib_data = get_spglib_data(cell=cell, atoms=atoms)
    # Or check that spglib data were *most likely* produced via wulfric's interface
    elif not isinstance(spglib_data, SyntacticSugar):
        raise TypeError(
            f"Are you sure that spglib_data were produced via wulfric's interface? Expected SyntacticSugar, got {type(spglib_data)}."
        )
    # Validate that user-provided spglib_data match user-provided structure
    else:
        validate_spglib_data(cell=cell, atoms=atoms, spglib_data=spglib_data)

    convention = convention.lower()

    # Straightforward interface to spglib
    # Primitive cell is rotated back to the original orientation of the given crystal
    if convention == "spglib":
        raise NotImplementedError

    elif convention == "hpkot":
        raise NotImplementedError
    elif convention == "sc":
        # lattice_type = None
        # matrix = SC_C_to_P[lattice_type]

        # primitive_cell = matrix.T @ conv_cell
        raise NotImplementedError

    else:
        raise ConventionNotSupported(
            convention, supported_conventions=["HPKOT", "SC", "spglib"]
        )


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
