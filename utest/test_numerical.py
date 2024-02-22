# Wulfric - Crystal, Lattice, Atoms, K-path.
# Copyright (C) 2023-2024 Andrey Rybakov
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

import pytest

from wulfric.numerical import compare_numerically


@pytest.mark.parametrize(
    "x, sign, y, result",
    [
        (-4, "==", -4.0, True),
        (-4.0, "==", -4, True),
        (-4.0, "==", -4.0, True),
        (-4.0, "==", 4.0, False),
        (-4.1, "==", 4.0, False),
        (4.00001, "==", 4.0, True),
    ],
)
def test_compare_numerically(x, sign, y, result):
    assert compare_numerically(x, sign, y) == result
