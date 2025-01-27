# Wulfric - Crystal, Lattice, Atoms, K-path.
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

import pytest

from wulfric.cell._basic_manipulation import params
from wulfric.cell._lepage import lepage
from wulfric.cell._sc_examples import cell_example
from wulfric.constants._numerical import EPS_LENGTH, EPS_RELATIVE
from wulfric.constants._sc_notation import BRAVAIS_LATTICE_VARIATIONS


################################################################################
#                                     LePage                                   #
################################################################################
@pytest.mark.parametrize(
    "variation", BRAVAIS_LATTICE_VARIATIONS, ids=BRAVAIS_LATTICE_VARIATIONS
)
def test_lepage(variation):
    cell = cell_example(variation)
    type_name = variation.translate(str.maketrans("", "", "12345ab"))
    assert lepage(*params(cell)) == type_name


@pytest.mark.parametrize(
    "cell, name, eps_relative",
    [
        (
            [[3.588, 0.000, 0.000], [0.000, 4.807, 0.000], [0.000, 0.000, 23.571]],
            "ORC",
            1e-3,
        ),
        (
            [[6.137, 0.000, 0.000], [-3.068, 5.315, 0.000], [0.000, 0.000, 20.718]],
            "HEX",
            1e-3,
        ),
    ],
    ids=["crsbr", "nii2"],
)
def test_custom_lepage(cell, name, eps_relative):
    assert lepage(*params(cell), eps_relative=eps_relative, eps_angle=0.01) == name


def test_lepage_paper():
    results = lepage(
        4,
        4.472,
        4.583,
        79.030,
        64.130,
        64.150,
        give_all_results=True,
        eps_relative=1e-3,
        eps_angle=0.006,
    )
    assert results[0][0] == "BCT"
    assert results[0][1] - 1.482 < 0.001
    assert results[1][0] == "ORCF"
    assert results[1][1] - 1.480 < 0.001
    assert results[2][0] == "ORCF"
    assert results[2][1] - 0.714 < 0.001
    assert results[3][0] == "MCLC"
    assert results[3][1] - 0.714 < 0.001
    assert results[4][0] == "MCLC"
    assert results[4][1] - 0.005 < 0.001


@pytest.mark.parametrize(
    "a, b, c, alpha, beta, gamma, ltype, eps_relative",
    [
        (1, 1, 2, 60, 90, 90, "TET", 1e-3),
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
def test_lepage_custom(a, b, c, alpha, beta, gamma, ltype, eps_relative):
    assert ltype == lepage(
        a, b, c, alpha, beta, gamma, eps_relative=eps_relative, eps_angle=0.01
    )


@pytest.mark.parametrize(
    "a, b, c, alpha, beta, gamma, ltype, eps_angle",
    [
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
        (
            4.0198877230381695,
            4.0198877230381695,
            40.16517980369646,
            90.01984696367262,
            90.01984696367262,
            59.99052495414632,
            "HEX",
            1e-1,
        ),
    ],
)
def test_lepage_custom_eps_angle(a, b, c, alpha, beta, gamma, ltype, eps_angle):
    assert ltype == lepage(
        a,
        b,
        c,
        alpha,
        beta,
        gamma,
        eps_angle=eps_angle,
    )
