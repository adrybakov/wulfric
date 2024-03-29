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

from math import acos, sqrt

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from wulfric.bravais_lattice.examples import lattice_example
from wulfric.constants import BRAVAIS_LATTICE_VARIATIONS, TODEGREES
from wulfric.identify import lepage, niggli
from wulfric.lattice import Lattice
from wulfric.numerical import ABS_TOL, ABS_TOL_ANGLE

################################################################################
#                               Service functions                              #
################################################################################
n_order = 5


def shuffle(cell, order):
    if order == 0:
        return [cell[2], cell[0], cell[1]]
    if order == 1:
        return [cell[1], cell[2], cell[0]]
    if order == 2:
        return cell
    if order == 3:
        return [cell[1], cell[0], cell[2]]
    if order == 4:
        return [cell[2], cell[1], cell[0]]
    if order == 5:
        return [cell[0], cell[2], cell[1]]


def rotate(cell, r1, r2, r3):
    R = Rotation.from_rotvec([r1, r2, r3]).as_matrix()
    return R.T @ cell


################################################################################
#                                     Niggli                                   #
################################################################################
# Křivý, I. and Gruber, B., 1976. A unified algorithm for determining the reduced (Niggli) cell.
# Acta Crystallographica Section A: Crystal Physics, Diffraction, Theoretical and General Crystallography, 32(2), pp.297-298.
def test_niggli_from_paper():
    a = 3
    b = sqrt(27)
    c = 2
    alpha = acos(-5 / 2 / sqrt(27) / 2) * TODEGREES
    beta = acos(-4 / 2 / 3 / 2) * TODEGREES
    gamma = acos(-22 / 2 / 3 / sqrt(27)) * TODEGREES
    assert (
        np.array([[4, 9, 9], [9 / 2, 3 / 2, 2]]) - niggli(a, b, c, alpha, beta, gamma)
        < ABS_TOL
    ).all()


def test_niggli_example():
    alpha = 79.030
    beta = 64.130
    gamma = 64.150
    a = 4
    b = 4.472
    c = 4.583
    ap, bp, cp, alphap, betap, gammap = niggli(
        a, b, c, alpha, beta, gamma, return_cell=True
    )

    assert a - ap < ABS_TOL
    assert b - bp < ABS_TOL
    assert c - cp < ABS_TOL
    assert alpha - alphap < ABS_TOL_ANGLE
    assert beta - betap < ABS_TOL_ANGLE
    assert gamma - gammap < ABS_TOL_ANGLE


def test_niggli_cell_volume_error():
    with pytest.raises(ValueError):
        niggli(1, 1, 1, 0, 0, 0)


# TODO: Is the finish of niggli guaranteed or not?
# @given(
#     st.floats(min_value=0, max_value=2 * pi),
#     st.floats(min_value=0, max_value=2 * pi),
#     st.floats(min_value=0, max_value=2 * pi),
#     st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     st.floats(min_value=MIN_ANGLE, max_value=180.0 - MIN_ANGLE),
#     st.floats(min_value=MIN_ANGLE, max_value=180.0 - MIN_ANGLE),
#     st.floats(min_value=MIN_ANGLE, max_value=180.0 - MIN_ANGLE),
#     st.integers(min_value=0, max_value=n_order),
# )
# def test_niggli_finish(r1, r2, r3, a, b, c, alpha, beta, gamma, order):
#     if parallelepiped_check(a, b, c, alpha, beta, gamma):
#         niggli(a, b, c, alpha, beta, gamma)


################################################################################
#                                     LePage                                   #
################################################################################
@pytest.mark.parametrize(
    "variation", BRAVAIS_LATTICE_VARIATIONS, ids=BRAVAIS_LATTICE_VARIATIONS
)
def test_lepage(variation):
    lattice = lattice_example(variation)
    type_name = variation.translate(str.maketrans("", "", "12345ab"))
    assert (
        lepage(
            lattice.a,
            lattice.b,
            lattice.c,
            lattice.alpha,
            lattice.beta,
            lattice.gamma,
        )
        == type_name
    )


@pytest.mark.parametrize(
    "cell, name, eps_rel",
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
def test_custom_lepage(cell, name, eps_rel):
    lattice = Lattice(cell)
    assert (
        lepage(
            lattice.a,
            lattice.b,
            lattice.c,
            lattice.alpha,
            lattice.beta,
            lattice.gamma,
            eps_rel=eps_rel,
        )
        == name
    )


def test_lepage_paper():
    results = lepage(
        4,
        4.472,
        4.583,
        79.030,
        64.130,
        64.150,
        give_all_results=True,
        eps_rel=1e-3,
        delta_max=0.006,
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
    "a, b, c, alpha, beta, gamma, ltype, eps_rel",
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
def test_lepage_custom(a, b, c, alpha, beta, gamma, ltype, eps_rel):
    assert ltype == lepage(
        a,
        b,
        c,
        alpha,
        beta,
        gamma,
        eps_rel=eps_rel,
    )


@pytest.mark.parametrize(
    "a, b, c, alpha, beta, gamma, ltype, delta_max",
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
def test_lepage_custom_delta_max(a, b, c, alpha, beta, gamma, ltype, delta_max):
    assert ltype == lepage(
        a,
        b,
        c,
        alpha,
        beta,
        gamma,
        delta_max=delta_max,
    )
