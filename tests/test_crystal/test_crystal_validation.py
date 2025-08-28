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
from wulfric.crystal._crystal_validation import validate_atoms
import pytest


@pytest.mark.parametrize(
    "atoms, required_keys, error",
    [
        # Can not count elements
        (dict(positions=42), None, TypeError),
        # Inconsistent amount of atoms
        (dict(names=["Cr1", "Cr2"], positions=[[0, 0, 0]]), None, ValueError),
        # Required key is missing
        (dict(), ["names"], ValueError),
        # positions not an array-like
        (dict(positions=[[0, 0, 0], [0.5, 0.5]]), None, ValueError),
        # Wrong shape of positions
        (dict(positions=[[0, 0], [0.5, 0.5]]), None, ValueError),
        # Name is not a string
        (dict(names=["Cr1", 42]), None, ValueError),
        # Species is not a string
        (dict(species=["Cr", 42]), None, ValueError),
        # Not a valid species
        (dict(species=["Cr1", "Cr2"]), None, ValueError),
        (dict(species=["CR", "Cr"]), None, ValueError),
        # Not an integer
        (dict(spglib_types=[1, 1.0]), None, ValueError),
        # Less than 1
        (dict(spglib_types=[1, 0]), None, ValueError),
    ],
)
def test_validate_atoms_fails(atoms, required_keys, error):
    with pytest.raises(error):
        validate_atoms(atoms=atoms, required_keys=required_keys)

    assert not validate_atoms(
        atoms=atoms, required_keys=required_keys, raise_errors=False
    )


@pytest.mark.parametrize(
    "atoms, required_keys",
    [
        # Empty dictionary
        (dict(), None),
        # Only names
        (dict(names=["Cr1", "Cr2"]), None),
        # Only names (required)
        (dict(names=["Cr1", "Cr2"]), ["names"]),
        # Only species
        (dict(species=["Cr", "Cr"]), None),
        # Only species (required)
        (dict(species=["Cr", "Cr"]), ["species"]),
        # Only positions
        (dict(positions=[[0, 0, 0]]), None),
        # Only positions (required)
        (dict(positions=[[0, 0, 0]]), ["positions"]),
        # Only spglib_types
        (dict(spglib_types=[1, 2, 3, 2]), None),
        # Only spglib_types (required)
        (dict(spglib_types=[1, 2, 3, 2]), ["spglib_types"]),
        # Species with an "X"
        (dict(species=["X", "Fe"]), None),
        # All keys
        (
            dict(
                names=["Cr1", "Cr2"],
                species=["Cr", "Cr"],
                positions=[[0, 0, 0], [0.5, 0.5, 0.5]],
                spglib_types=[1, 2],
            ),
            None,
        ),
        # All keys (required)
        (
            dict(
                names=["Cr1", "Cr2"],
                species=["Cr", "Cr"],
                positions=[[0, 0, 0], [0.5, 0.5, 0.5]],
                spglib_types=[1, 2],
            ),
            ["names", "species", "positions", "spglib_types"],
        ),
        # Extra keys
        (
            dict(
                names=["Cr1", "Cr2"],
                species=["Cr", "Cr"],
                positions=[[0, 0, 0], [0.5, 0.5, 0.5]],
                spins=[3 / 2, 3 / 2],
            ),
            None,
        ),
        # Extra keys (required)
        (
            dict(
                names=["Cr1", "Cr2"],
                species=["Cr", "Cr"],
                positions=[[0, 0, 0], [0.5, 0.5, 0.5]],
                spins=[3 / 2, 3 / 2],
            ),
            ["spins"],
        ),
    ],
)
def test_validate_atoms_passes(atoms, required_keys):
    assert validate_atoms(atoms=atoms, required_keys=required_keys, raise_errors=False)
