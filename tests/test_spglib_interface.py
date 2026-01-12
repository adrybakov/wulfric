# ================================== LICENSE ===================================
# Wulfric - Cell, Atoms, K-path, visualization.
# Copyright (C) 2023-2026 Andrey Rybakov
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

import pytest
from wulfric._spglib_interface import get_spglib_types


@pytest.mark.parametrize(
    "atoms, expected_types",
    [
        # Already present
        (dict(spglib_types=[1, 2, 2, 2, 3]), [1, 2, 2, 2, 3]),
        # Deduced from species
        (dict(species=["Cr", "Cr", "Fe"]), [1, 1, 2]),
        # Deduced from names
        (dict(names=["Cr1", "Cr2", "Fe"]), [1, 1, 2]),
        # All present
        (
            dict(
                spglib_types=[1, 1, 2],
                names=["Cr1", "Fe", "Cr2"],
                species=["Cr", "Fe", "Cr"],
            ),
            [1, 1, 2],
        ),
        # Names and species
        (
            dict(
                names=["Cr1", "Fe", "Cr2"],
                species=["Cr", "Cr", "Fe"],
            ),
            [1, 1, 2],
        ),
    ],
)
def test_get_spglib_types(atoms, expected_types):
    spglib_types = get_spglib_types(atoms=atoms)

    assert spglib_types == expected_types
