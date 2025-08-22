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
import pytest

from wulfric._lepage import lepage
from wulfric.cell._basic_manipulation import from_params
from wulfric.cell._sc_examples import get_example_cell_SC
from wulfric.constants._sc_convention import SC_BRAVAIS_LATTICE_VARIATIONS


################################################################################
#                                     LePage                                   #
################################################################################
@pytest.mark.parametrize(
    "variation", SC_BRAVAIS_LATTICE_VARIATIONS, ids=SC_BRAVAIS_LATTICE_VARIATIONS
)
def test_lepage(variation):
    cell = get_example_cell_SC(variation)
    type_name = variation.translate(str.maketrans("", "", "12345ab"))
    assert lepage(cell) == type_name


@pytest.mark.parametrize(
    "a, b, c, alpha, beta, gamma, ltype, angle_tolerance",
    [
        (1, 1, 2, 90, 90, 60, "HEX", 1e-3),
        (1, 1, 1, 30, 90, 90, "ORCC", 1e-3),
        (1, 1, 1, 45, 90, 90, "ORCC", 1e-3),
        (3.2, 1, 1, 45, 90, 90, "ORCC", 1e-3),
        (1, 1, 1, 60, 90, 90, "HEX", 1e-3),
        (
            4.0198877230381695,
            4.0198877230381695,
            40.16517980369646,
            90.01984696367262,
            90.01984696367262,
            59.99052495414632,
            "TRI",
            1e-3,
        ),
    ],
)
def test_lepage_from_params(a, b, c, alpha, beta, gamma, ltype, angle_tolerance):
    cell = from_params(a, b, c, alpha, beta, gamma)
    assert ltype == lepage(cell, angle_tolerance=angle_tolerance)


@pytest.mark.parametrize(
    "cell, name, angle_tolerance",
    [
        (
            [[3.588, 0.000, 0.000], [0.000, 4.807, 0.000], [0.000, 0.000, 23.571]],
            "ORC",
            1e-4,
        ),
        (
            [[6.137, 0.000, 0.000], [-3.068, 5.315, 0.000], [0.000, 0.000, 20.718]],
            "HEX",
            1e-2,
        ),
        (
            [[6.137, 0.000, 0.000], [-3.068, 5.315, 0.000], [0.000, 0.000, 20.718]],
            "MCL",
            1e-5,
        ),
    ],
    ids=["crsbr", "nii2-hex", "nii2-mcl"],
)
def test_lepage_from_cell(cell, name, angle_tolerance):
    assert lepage(cell, angle_tolerance=angle_tolerance) == name


@pytest.mark.parametrize(
    "name, angle_tolerance",
    [("BCT", 2), ("ORCF", 1), ("MCLC", 0.006)],
)
def test_lepage_paper(name, angle_tolerance):
    cell = from_params(
        4,
        4.472,
        4.583,
        79.030,
        64.130,
        64.150,
    )
    lattice_type = lepage(cell, angle_tolerance=angle_tolerance)
    assert lattice_type == name
