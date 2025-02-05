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


from math import acos, sqrt

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from wulfric.cell._basic_manipulation import from_params, get_params
from wulfric.cell._niggli import niggli
from wulfric.constants._numerical import TODEGREES

################################################################################
#                               Service functions                              #
################################################################################
N_ORDER = 5


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
#                                  Test Niggli                                 #
################################################################################
# Křivý, I. and Gruber, B., 1976.
# A unified algorithm for determining the reduced (Niggli) cell.
# Acta Crystallographica Section A: Crystal Physics, Diffraction, Theoretical and General
# Crystallography, 32(2), pp.297-298.
# def test_niggli_from_paper():
#     a = 3
#     b = sqrt(27)
#     c = 2
#     alpha = acos(-5 / 2 / sqrt(27) / 2) * TODEGREES
#     beta = acos(-4 / 2 / 3 / 2) * TODEGREES
#     gamma = acos(-22 / 2 / 3 / sqrt(27)) * TODEGREES
#     cell = from_params(a,b,c,alpha,beta,gamma)
#     assert np.allclose(
#         np.array([[4, 9, 9], [9 / 2, 3 / 2, 2]]),
#         niggli(cell),
#         atol=EPS_LENGTH,
#         rtol=EPS_LENGTH,
#     )


def test_niggli_example():
    alpha = 79.030
    beta = 64.130
    gamma = 64.150
    a = 4
    b = 4.472
    c = 4.583
    ap, bp, cp, alphap, betap, gammap = get_params(
        niggli(from_params(a, b, c, alpha, beta, gamma))
    )

    assert abs(a - ap) < 1e-3
    assert abs(b - bp) < 1e-3
    assert abs(c - cp) < 1e-3
    assert abs(alpha - alphap) < 1e-3
    assert abs(beta - betap) < 1e-3
    assert abs(gamma - gammap) < 1e-3


def test_niggli_cell_volume_error():
    with pytest.raises(ValueError):
        niggli([[0, 0, 0], [0, 1, 0], [0, 0, 1]])
