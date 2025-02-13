# Wulfric - Cell, Atoms, K-path.
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


import os
from calendar import month_name
from datetime import datetime

import numpy as np

from wulfric._decorate_array import print_2d_array
from wulfric.crystal._atoms import get_atom_species
from wulfric.geometry._geometry import absolute_to_relative, get_volume

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def load_poscar(file_object=None, return_comment=False):
    r"""
    Reads crystal structure from the |POSCAR|_ file.

    Parameters
    ----------
    file_object : str of file-like object, optional
        File to be read. If str, then file is opened with the given name.
        Otherwise it has to have ``.readlines()`` method. By default it looks for the
        "POSCAR" file in the current directory. Behaviour for ``str``:

        * Tries to open the file with the name  ``file_object``.
        * Tries to open the file with the name "POSCAR" in the directory ``file_object``.

    return_comment : bool, default False
        Whether to return the comment from the first line of the POSCAR file.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Cell of a crystal structure, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]
    atoms : dict
        Atoms of the crystal structure.
        Positions are always relative to the cell.
    comment : str
        Comment from the first line of the file. If ``return_comment`` is ``True``.

    Examples
    --------

    .. doctest::

        >>> # Load a POSCAR file
        >>> cell, atoms = wulf.io.load_poscar('POSCAR') # doctest: +SKIP
        >>> # It can return the comment from the file as well:
        >>> cell, atoms, comment = wulf.io.load_poscar('POSCAR', return_comment=True) # doctest: +SKIP

    """

    # Open file if needed
    if file_object is None:
        try:
            file_object = open("POSCAR")
        except FileNotFoundError:
            raise FileNotFoundError(
                f'"POSCAR" file not found, looked here: {os.getcwd()}'
            )
    elif isinstance(file_object, str):
        try:
            file_object = open(file_object, "r", encoding="utf-8")
        except FileNotFoundError:
            try:
                file_object = open(
                    os.path.join(file_object, "POSCAR"), "r", encoding="utf-8"
                )
            except FileNotFoundError:
                raise FileNotFoundError(
                    f'"POSCAR" file not found, looked here: {file_object}'
                )

    lines = file_object.readlines()

    comment = lines[0].strip()

    # 1 or 3 numbers
    scale_factor = np.array(list(map(float, lines[1].split())))
    cell = np.array(list(map(lambda x: list(map(float, x.split())), lines[2:5])))
    if len(scale_factor) == 1:
        if scale_factor[0] < 0:
            scale_factor = abs(scale_factor[0] / get_volume(cell))
        cell *= scale_factor
    elif len(scale_factor) == 3 and np.all(scale_factor > 0):
        cell[0] *= scale_factor[0]
        cell[1] *= scale_factor[1]
        cell[2] *= scale_factor[2]
    else:
        raise ValueError(
            "Scale factor has to be a single positive ot negative number or "
            + f"a list of 3 positive numbers, got: {scale_factor}"
        )
    # Read species name and numbers
    species = lines[5].split()
    GOT_SPECIES_NAMES = False
    index = 6
    for i in species:
        try:
            int(i)
        except ValueError:
            GOT_SPECIES_NAMES = True
    if GOT_SPECIES_NAMES:
        species_names = species
        species = lines[6].split()
        index = 7
    else:
        species_names = None
    ions_per_species = list(map(int, species))

    # Skip selective dynamics
    if lines[index][0] in ["S", "s"]:
        index += 1

    # Get mode
    CARTESIAN = False
    if lines[index][0].lower() in ["c", "k"]:
        CARTESIAN = True
    index += 1
    atoms = {"names": [], "positions": []}
    for i in range(len(species)):
        for j in range(ions_per_species[i]):
            coordinates = np.array(list(map(float, lines[index].split()[:3])))
            index += 1
            if CARTESIAN:
                # Both cases (1 or 3 numbers) are covered
                coordinates *= scale_factor
                coordinates = absolute_to_relative(coordinates, cell)
            if species_names is None:
                atoms["names"].append(f"X{i+1}")
                atoms["positions"].append(coordinates)
            else:
                atoms["names"].append(species_names[i])
                atoms["positions"].append(coordinates)

    if return_comment:
        return cell, atoms, comment
    return cell, atoms


def dump_poscar(
    cell,
    atoms,
    file_object="POSCAR",
    comment: str = None,
    decimals=8,
    mode: str = "Direct",
):
    r"""
    Writes crystal structure to the |POSCAR|_ file.

    Parameters
    ----------
    cell : (3, 3) |array-like|_,
        Matrix of a cell, rows are interpreted as vectors.
    atoms : dict
        Dictionary with atoms. Must have a ``"positions"`` with value of (N,3)
        |array-like|_. Must have either ``"names"`` key with value of ``list`` of ``str``
        of length N or ``"species"`` key with value of ``list`` of ``str`` of length N.
        If ``"species"`` key is not present, try to deduce atom's species from
        ``"names"``, raise error on fail.
    file_object : str of file-like object, optional
        File to be written. If str, then file is opened with the given name.
        Otherwise it has to have ``.write()`` method.
    comment : str, optional
        Comment to be written in the first line of the file. Has to be a single line.
        All new lines symbols are replaced with spaces.
    decimals : int, default 8
        Number of decimals to be written.
    mode : str, default "Direct"
        Mode of the coordinates to be written. Can be "Direct" or "Cartesian".

    Examples
    --------

    .. doctest::

        >>> # Dump a POSCAR file
        >>> wulf.io.dump_poscar(cell, atoms, 'POSCAR') # doctest: +SKIP
        >>> # If you want to write a comment as well:
        >>> wulf.io.dump_poscar(cell, atoms, 'POSCAR', comment='This is a comment') # doctest: +SKIP
        >>> # You can control the amount of decimals in the output:
        >>> wulf.io.dump_poscar(cell, atoms, 'POSCAR', decimals=6) # doctest: +SKIP
        >>> # You can switch the mode of coordinates between 'Cartesian' and 'Direct' (default):
        >>> wulf.io.dump_poscar(cell, atoms, 'POSCAR', mode="Cartesian") # doctest: +SKIP

    """

    cell = np.array(cell, dtype=float)

    # Prepare comment
    if comment is None:
        cd = datetime.now()
        comment = (
            f"Written by wulfric (wulfric.org) "
            f"on {cd.day} {month_name[cd.month]} {cd.year} "
            f"at {cd.hour}:{cd.minute}:{cd.second}"
        )
    else:
        comment = comment.replace("\n", " ")

    # Check mode
    if mode not in ("Direct", "Cartesian"):
        raise ValueError(f'mode has to be "Direct" or "Cartesian", given: {mode}')

    # Prepare atoms
    atoms_list = []
    for i in range(len(atoms["positions"])):
        if "species" in atoms:
            atom_type = atoms["species"][i]
        else:
            atom_type = get_atom_species(atoms["names"][i])
            if atom_type == "X":
                raise ValueError(
                    f"Can not deduce atom's type from the name '{atoms['name'][i]}', while dumping to POSCAR."
                )
        if mode == "Direct":
            atom_position = atoms["positions"][i]
        else:
            atom_position = atoms["positions"][i] @ cell

        atoms_list.append((atom_type, atom_position))

    # Sort atoms by type
    atoms_list = sorted(atoms_list, key=lambda x: x[0])

    # Prepare atom species and coordinates
    atom_species = {}
    atom_coordinates = []
    for atom in atoms_list:
        if atom[0] not in atom_species:
            atom_species[atom[0]] = 1
        else:
            atom_species[atom[0]] += 1
        atom_coordinates.append(atom[1])

    # Open file if needed
    if isinstance(file_object, str):
        file_object = open(file_object, "w", encoding="utf-8")

    # Write
    file_object.write(comment + "\n")
    file_object.write("1.0\n")
    file_object.write(
        print_2d_array(cell, fmt=f".{decimals}f", print_result=False, borders=False)
        + "\n"
    )

    for species in atom_species:
        file_object.write(f"{species} ")
    file_object.write("\n")
    for species in atom_species:
        file_object.write(f"{atom_species[species]} ")
    file_object.write("\n")

    file_object.write(mode + "\n")
    file_object.write(
        print_2d_array(
            atom_coordinates, fmt=f".{decimals}f", print_result=False, borders=False
        )
        + "\n"
    )


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
