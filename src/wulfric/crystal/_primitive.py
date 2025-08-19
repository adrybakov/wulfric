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


# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def get_primitive(
    cell,
    atoms,
    convention="HPKOT",
    spglib_symprec=1e-5,
    spglib_angle_tolerance=-1,
):
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
        Conventional cell.
    primitive_atoms : dict
        Dictionary of atoms of the conventional cell. Has all the same keys as the
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
    ``types`` for given atoms see :ref:`wulfric.crystal.get_spglib_types()`.

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
    raise NotImplementedError


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
