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


from math import acos, cos, pi, sqrt

import numpy as np
from hypothesis import example, given
from hypothesis import strategies as st
from scipy.spatial.transform import Rotation

from wulfric._exceptions import StandardizationTypeMismatch
from wulfric._numerical import compare_numerically
from wulfric.cell._basic_manipulation import get_reciprocal, is_reasonable, params
from wulfric.cell._sc_constructors import (
    BCC,
    BCT,
    CUB,
    FCC,
    HEX,
    MCL,
    MCLC,
    ORC,
    ORCC,
    ORCF,
    ORCI,
    RHL,
    TET,
    TRI,
)
from wulfric.cell._sc_standardize import (
    _BCC_get_S_matrix,
    _BCT_get_S_matrix,
    _CUB_get_S_matrix,
    _FCC_get_S_matrix,
    _HEX_get_S_matrix,
    _MCL_get_S_matrix,
    _MCLC_get_S_matrix,
    _ORC_get_S_matrix,
    _ORCC_get_S_matrix,
    _ORCF_get_S_matrix,
    _ORCI_get_S_matrix,
    _RHL_get_S_matrix,
    _TET_get_S_matrix,
    _TRI_get_S_matrix,
)
from wulfric.constants._numerical import (
    EPS_ANGLE,
    EPS_LENGTH,
    EPS_RELATIVE,
    MIN_ANGLE,
    TODEGREES,
    TORADIANS,
)
from wulfric.geometry._geometry import parallelepiped_check

################################################################################
#                               Service routines                               #
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
    return cell @ R.T


################################################################################
#                                      CUB                                     #
################################################################################
@given(
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.integers(min_value=0, max_value=n_order),
)
def test_CUB_get_S_matrix(r1, r2, r3, conv_a, order):
    if not np.allclose([r1, r2, r3], [0, 0, 0], rtol=EPS_RELATIVE, atol=EPS_LENGTH):
        # Prepare cell
        cell = shuffle(rotate(CUB(conv_a), r1, r2, r3), order)
        if is_reasonable(cell):
            old_det = np.linalg.det(cell)

            # Fix cell
            S = _CUB_get_S_matrix(cell, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            cell = np.linalg.inv(S.T) @ cell

            # Check results
            a, b, c, alpha, beta, gamma = params(cell)
            assert np.allclose([a, b, c], [a, a, a], rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            assert np.allclose(
                [alpha, beta, gamma],
                [90.0, 90.0, 90.0],
                rtol=EPS_RELATIVE,
                atol=EPS_ANGLE,
            )

            # Check that chirality is the same
            assert np.linalg.det(cell) * old_det > 0


################################################################################
#                                      FCC                                     #
################################################################################
@given(
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0.0, allow_infinity=False, allow_nan=False),
    st.integers(min_value=0, max_value=n_order),
)
def test_FCC_get_S_matrix(r1, r2, r3, conv_a, order):
    if not np.allclose([r1, r2, r3], [0, 0, 0], rtol=EPS_RELATIVE, atol=EPS_LENGTH):
        # Prepare cell
        cell = shuffle(rotate(FCC(conv_a), r1, r2, r3), order)
        if is_reasonable(cell):
            prim_a = conv_a * sqrt(2) / 2
            old_det = np.linalg.det(cell)

            # Fix cell
            S = _FCC_get_S_matrix(cell, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            cell = np.linalg.inv(S.T) @ cell

            # Check results
            a, b, c, alpha, beta, gamma = params(cell)
            assert np.allclose(
                [a, b, c], [prim_a, prim_a, prim_a], rtol=EPS_RELATIVE, atol=EPS_LENGTH
            )
            assert np.allclose(
                [alpha, beta, gamma],
                [60.0, 60.0, 60.0],
                rtol=EPS_RELATIVE,
                atol=EPS_ANGLE,
            )

            # Check that chirality is the same
            assert np.linalg.det(cell) * old_det > 0


################################################################################
#                                      BCC                                     #
################################################################################
@given(
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.integers(min_value=0, max_value=n_order),
)
def test_BCC_get_S_matrix(r1, r2, r3, conv_a, order):
    if not np.allclose([r1, r2, r3], [0, 0, 0], rtol=EPS_RELATIVE, atol=EPS_LENGTH):
        # Prepare cell
        cell = shuffle(rotate(BCC(conv_a), r1, r2, r3), order)
        if is_reasonable(cell):
            angle = acos(-1 / 3) * TODEGREES
            prim_a = conv_a * sqrt(3) / 2
            old_det = np.linalg.det(cell)

            # Fix cell
            S = _BCC_get_S_matrix(cell, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            cell = np.linalg.inv(S.T) @ cell

            # Check results
            a, b, c, alpha, beta, gamma = params(cell)
            assert np.allclose(
                [a, b, c], [prim_a, prim_a, prim_a], rtol=EPS_RELATIVE, atol=EPS_LENGTH
            )
            assert np.allclose(
                [alpha, beta, gamma],
                [angle, angle, angle],
                rtol=EPS_RELATIVE,
                atol=EPS_ANGLE,
            )

            # Check that chirality is the same
            assert np.linalg.det(cell) * old_det > 0


################################################################################
#                                      TET                                     #
################################################################################
@given(
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.integers(min_value=0, max_value=n_order),
)
def test_TET_get_S_matrix(r1, r2, r3, conv_a, conv_c, order):
    if not np.allclose([r1, r2, r3], [0, 0, 0], rtol=EPS_RELATIVE, atol=EPS_LENGTH):
        # Prepare cell
        cell = shuffle(rotate(TET(conv_a, conv_c), r1, r2, r3), order)
        if is_reasonable(cell):
            angle = 90
            prim_a = conv_a
            prim_c = conv_c
            old_det = np.linalg.det(cell)

            # Fix cell
            try:
                S = _TET_get_S_matrix(cell, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            except StandardizationTypeMismatch:
                return
            cell = np.linalg.inv(S.T) @ cell

            # Check results
            a, b, c, alpha, beta, gamma = params(cell)
            assert np.allclose(
                [a, b, c],
                [prim_a, prim_a, prim_c],
                rtol=EPS_RELATIVE,
                atol=EPS_LENGTH,
            )
            assert np.allclose(
                [alpha, beta, gamma],
                [angle, angle, angle],
                rtol=EPS_RELATIVE,
                atol=EPS_ANGLE,
            )

            # Check that chirality is the same
            assert np.linalg.det(cell) * old_det > 0


################################################################################
#                                      BCT                                     #
################################################################################
@given(
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.integers(min_value=0, max_value=n_order),
)
def test_BCT_get_S_matrix(r1, r2, r3, conv_a, conv_c, order):
    if not np.allclose([r1, r2, r3], [0, 0, 0], rtol=EPS_RELATIVE, atol=EPS_LENGTH):
        # Prepare cell
        cell = shuffle(rotate(BCT(conv_a, conv_c), r1, r2, r3), order)
        if is_reasonable(cell):
            prim = sqrt(2 * conv_a**2 + conv_c**2) / 2
            angle12 = acos((conv_c**2 - 2 * conv_a**2) / 4 / prim**2)
            angle = acos(-(conv_c**2) / 4 / prim**2)
            old_det = np.linalg.det(cell)

            # Fix cell
            try:
                S = _BCT_get_S_matrix(cell, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            except StandardizationTypeMismatch:
                return
            cell = np.linalg.inv(S.T) @ cell

            # Check results
            a, b, c, alpha, beta, gamma = params(cell)
            alpha *= TORADIANS
            beta *= TORADIANS
            gamma *= TORADIANS
            assert np.allclose(
                [a, b, c], [prim, prim, prim], rtol=EPS_RELATIVE, atol=EPS_LENGTH
            )
            assert np.allclose(
                [alpha, beta, gamma],
                [angle, angle, angle12],
                rtol=EPS_RELATIVE,
                atol=EPS_ANGLE,
            )

            # Check that chirality is the same
            assert np.linalg.det(cell) * old_det > 0


################################################################################
#                                      ORC                                     #
################################################################################
@given(
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.integers(min_value=0, max_value=n_order),
)
def test_ORC_get_S_matrix(r1, r2, r3, conv_a, conv_b, conv_c, order):
    if not np.allclose([r1, r2, r3], [0, 0, 0], rtol=EPS_RELATIVE, atol=EPS_LENGTH):
        # Prepare cell
        cell = shuffle(rotate(ORC(conv_a, conv_b, conv_c), r1, r2, r3), order)
        if is_reasonable(cell):
            prim_a, prim_b, prim_c = sorted([conv_a, conv_b, conv_c])
            angle = 90
            old_det = np.linalg.det(cell)

            # Fix cell
            try:
                S = _ORC_get_S_matrix(cell, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            except StandardizationTypeMismatch:
                return
            cell = np.linalg.inv(S.T) @ cell

            # Check results
            a, b, c, alpha, beta, gamma = params(cell)
            assert np.allclose(
                [a, b, c], [prim_a, prim_b, prim_c], rtol=EPS_RELATIVE, atol=EPS_LENGTH
            )
            assert np.allclose(
                [alpha, beta, gamma],
                [angle, angle, angle],
                rtol=EPS_RELATIVE,
                atol=EPS_ANGLE,
            )

            # Check that chirality is the same
            assert np.linalg.det(cell) * old_det > 0


################################################################################
#                                     ORCF                                     #
################################################################################
@given(
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.integers(min_value=0, max_value=n_order),
)
def test_ORCF_get_S_matrix(r1, r2, r3, conv_a, conv_b, conv_c, order):
    if not np.allclose([r1, r2, r3], [0, 0, 0], rtol=EPS_RELATIVE, atol=EPS_LENGTH):
        # Prepare cell
        cell = shuffle(rotate(ORCF(conv_a, conv_b, conv_c), r1, r2, r3), order)
        if is_reasonable(cell):
            conv_a, conv_b, conv_c = sorted([conv_a, conv_b, conv_c])
            prim_a = sqrt(conv_b**2 + conv_c**2) / 2.0
            prim_b = sqrt(conv_a**2 + conv_c**2) / 2.0
            prim_c = sqrt(conv_a**2 + conv_b**2) / 2.0
            prim_alpha = acos(conv_a**2 / 4.0 / prim_b / prim_c) * TODEGREES
            prim_alpha_twin = 180.0 - prim_alpha
            prim_beta = acos(conv_b**2 / 4.0 / prim_a / prim_c) * TODEGREES
            prim_beta_twin = 180.0 - prim_beta
            prim_gamma = acos(conv_c**2 / 4.0 / prim_a / prim_b) * TODEGREES
            prim_gamma_twin = 180.0 - prim_gamma
            old_det = np.linalg.det(cell)

            # Fix cell
            try:
                S = _ORCF_get_S_matrix(cell, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            except StandardizationTypeMismatch:
                return

            cell = np.linalg.inv(S.T) @ cell

            # Check results
            a, b, c, alpha, beta, gamma = params(cell)
            assert np.allclose(
                [a, b, c], [prim_a, prim_b, prim_c], rtol=EPS_RELATIVE, atol=EPS_LENGTH
            )
            assert np.allclose(
                alpha, prim_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE
            ) or np.allclose(alpha, prim_alpha_twin, rtol=EPS_RELATIVE, atol=EPS_ANGLE)
            assert np.allclose(
                beta, prim_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE
            ) or np.allclose(beta, prim_beta_twin, rtol=EPS_RELATIVE, atol=EPS_ANGLE)
            assert np.allclose(
                gamma, prim_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE
            ) or np.allclose(gamma, prim_gamma_twin, rtol=EPS_RELATIVE, atol=EPS_ANGLE)

            # Check that chirality is the same
            assert np.linalg.det(cell) * old_det > 0


################################################################################
#                                     ORCI                                     #
################################################################################
@given(
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.integers(min_value=0, max_value=n_order),
)
def test_ORCI_get_S_matrix(r1, r2, r3, conv_a, conv_b, conv_c, order):
    if not np.allclose([r1, r2, r3], [0, 0, 0], rtol=EPS_RELATIVE, atol=EPS_LENGTH):
        # Prepare cell
        cell = shuffle(rotate(ORCI(conv_a, conv_b, conv_c), r1, r2, r3), order)
        if is_reasonable(cell):
            conv_a, conv_b, conv_c = sorted([conv_a, conv_b, conv_c])
            prim = sqrt(conv_a**2 + conv_b**2 + conv_c**2) / 2
            prim_alpha = (
                acos((conv_a**2 - conv_b**2 - conv_c**2) / 4.0 / prim**2) * TODEGREES
            )
            prim_alpha_twin = 180.0 - prim_alpha
            prim_beta = (
                acos((-(conv_a**2) + conv_b**2 - conv_c**2) / 4.0 / prim**2) * TODEGREES
            )
            prim_beta_twin = 180.0 - prim_beta
            prim_gamma = (
                acos((-(conv_a**2) - conv_b**2 + conv_c**2) / 4.0 / prim**2) * TODEGREES
            )
            prim_gamma_twin = 180.0 - prim_gamma
            old_det = np.linalg.det(cell)

            # Fix cell
            try:
                S = _ORCI_get_S_matrix(cell, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            except StandardizationTypeMismatch:
                return
            cell = np.linalg.inv(S.T) @ cell

            # Check results
            a, b, c, alpha, beta, gamma = params(cell)
            assert np.allclose(
                [a, b, c], [prim, prim, prim], rtol=EPS_RELATIVE, atol=EPS_LENGTH
            )
            assert np.allclose(
                alpha, prim_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE
            ) or np.allclose(alpha, prim_alpha_twin, rtol=EPS_RELATIVE, atol=EPS_ANGLE)
            assert np.allclose(
                beta, prim_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE
            ) or np.allclose(beta, prim_beta_twin, rtol=EPS_RELATIVE, atol=EPS_ANGLE)
            assert np.allclose(
                gamma, prim_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE
            ) or np.allclose(gamma, prim_gamma_twin, rtol=EPS_RELATIVE, atol=EPS_ANGLE)

            # Check that chirality is the same
            assert np.linalg.det(cell) * old_det > 0


################################################################################
#                                     ORCC                                     #
################################################################################
@example(r1=0.0, r2=0.0, r3=1.0, conv_a=1.0, conv_b=0.0078125, conv_c=0.5, order=0)
@example(r1=0.0, r2=0.0, r3=1.0, conv_a=1.0, conv_b=1.0, conv_c=0.5, order=0)
@example(
    r1=0.0,
    r2=1.0,
    r3=0.0078125,
    conv_a=314768.08572113514,
    conv_b=314768.08572113514,
    conv_c=362.0,
    order=0,
)
@given(
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.integers(min_value=0, max_value=n_order),
)
def test_ORCC_get_S_matrix(r1, r2, r3, conv_a, conv_b, conv_c, order):
    if (
        not np.allclose([r1, r2, r3], [0, 0, 0], rtol=EPS_RELATIVE, atol=EPS_LENGTH)
        and compare_numerically(conv_a, "!=", conv_b)
        and compare_numerically(conv_a, "!=", conv_c)
        and compare_numerically(conv_b, "!=", conv_c)
    ):
        cell = shuffle(rotate(ORCC(conv_a, conv_b, conv_c), r1, r2, r3), order)
        if is_reasonable(cell):

            conv_a, conv_b = sorted([conv_a, conv_b])
            prim_a = sqrt(conv_a**2 + conv_b**2) / 2
            prim_b = prim_a
            prim_c = conv_c
            prim_alpha = 90.0
            prim_beta = prim_alpha
            prim_gamma = (
                acos((conv_a**2 - conv_b**2) / 4.0 / prim_a / prim_b) * TODEGREES
            )

            old_det = np.linalg.det(cell)

            # Fix the cell
            try:
                S = _ORCC_get_S_matrix(cell, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            except StandardizationTypeMismatch:
                return
            cell = np.linalg.inv(S.T) @ cell

            # Check results
            a, b, c, alpha, beta, gamma = params(cell)
            assert np.allclose(
                [a, b, c], [prim_a, prim_b, prim_c], rtol=EPS_RELATIVE, atol=EPS_LENGTH
            )
            assert np.allclose(
                alpha, prim_alpha, rtol=EPS_RELATIVE, atol=EPS_LENGTH
            ) or np.allclose(
                alpha, 180.0 - prim_alpha, rtol=EPS_RELATIVE, atol=EPS_LENGTH
            )
            assert np.allclose(
                beta, prim_beta, rtol=EPS_RELATIVE, atol=EPS_LENGTH
            ) or np.allclose(
                beta, 180.0 - prim_beta, rtol=EPS_RELATIVE, atol=EPS_LENGTH
            )
            assert np.allclose(
                gamma, prim_gamma, rtol=EPS_RELATIVE, atol=EPS_LENGTH
            ) or np.allclose(
                gamma, 180.0 - prim_gamma, rtol=EPS_RELATIVE, atol=EPS_LENGTH
            )

            # Check that chirality is the same
            assert np.linalg.det(cell) * old_det > 0


################################################################################
#                                     HEX                                      #
################################################################################
@given(
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.integers(min_value=0, max_value=n_order),
)
def test_HEX_get_S_matrix(r1, r2, r3, conv_a, conv_c, order):
    if not np.allclose([r1, r2, r3], [0, 0, 0], rtol=EPS_RELATIVE, atol=EPS_LENGTH):
        # Prepare cell
        cell = shuffle(rotate(HEX(conv_a, conv_c), r1, r2, r3), order)
        if is_reasonable(cell):
            prim_a = conv_a
            prim_b = conv_a
            prim_c = conv_c
            prim_alpha = 90.0
            prim_beta = 90.0
            prim_gamma = 120.0
            old_det = np.linalg.det(cell)

            # Fix cell
            try:
                S = _HEX_get_S_matrix(cell, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            except StandardizationTypeMismatch:
                return
            cell = np.linalg.inv(S.T) @ cell

            # Check results
            a, b, c, alpha, beta, gamma = params(cell)
            assert np.allclose(
                [a, b, c], [prim_a, prim_b, prim_c], rtol=EPS_RELATIVE, atol=EPS_LENGTH
            )
            assert np.allclose(alpha, prim_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE)
            assert np.allclose(beta, prim_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE)
            assert np.allclose(gamma, prim_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE)

            # Check that chirality is the same
            assert np.linalg.det(cell) * old_det > 0


################################################################################
#                                     RHL                                      #
################################################################################
@example(
    r1=0.0,
    r2=0.0,
    r3=1.0,
    conv_a=1.0,
    conv_alpha=1.0,
    order=3,
)
@given(
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=MIN_ANGLE, max_value=120.0 - MIN_ANGLE),
    st.integers(min_value=0, max_value=n_order),
)
def test_RHL_get_S_matrix(r1, r2, r3, conv_a, conv_alpha, order):
    if not np.allclose([r1, r2, r3], [0, 0, 0], rtol=EPS_RELATIVE, atol=EPS_LENGTH):
        # Prepare cell
        cell = shuffle(rotate(RHL(conv_a, conv_alpha), r1, r2, r3), order)
        if is_reasonable(cell):
            prim_a = conv_a
            prim_b = conv_a
            prim_c = conv_a
            prim_alpha = conv_alpha
            prim_beta = conv_alpha
            prim_gamma = conv_alpha
            old_det = np.linalg.det(cell)

            # Fix cell
            S = _RHL_get_S_matrix(cell, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            cell = np.linalg.inv(S.T) @ cell

            # Check results
            a, b, c, alpha, beta, gamma = params(cell)
            assert np.allclose(
                [a, b, c], [prim_a, prim_b, prim_c], rtol=EPS_RELATIVE, atol=EPS_LENGTH
            )
            assert np.allclose(alpha, prim_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE)
            assert np.allclose(beta, prim_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE)
            assert np.allclose(gamma, prim_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE)

            # Check that chirality is the same
            assert np.linalg.det(cell) * old_det > 0


################################################################################
#                                     MCL                                      #
################################################################################
@example(
    r1=0.0, r2=0.0, r3=1.0, conv_a=1.0, conv_b=1.0, conv_c=1.0, conv_alpha=1.0, order=3
)
@example(
    r1=0.0, r2=0.0, r3=1.0, conv_a=1.0, conv_b=1.0, conv_c=2.0, conv_alpha=90.0, order=0
)
@example(
    r1=0.0, r2=0.0, r3=1.0, conv_a=1.0, conv_b=1.0, conv_c=2.0, conv_alpha=91, order=0
)
@given(
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=MIN_ANGLE, max_value=180.0 - MIN_ANGLE),
    st.integers(min_value=0, max_value=n_order),
)
def test_MCL_get_S_matrix(r1, r2, r3, conv_a, conv_b, conv_c, conv_alpha, order):
    if not np.allclose(
        [r1, r2, r3], [0, 0, 0], rtol=EPS_RELATIVE, atol=EPS_LENGTH
    ) and compare_numerically(
        conv_alpha, "!=", 90.0, rtol=EPS_RELATIVE, atol=EPS_ANGLE
    ):
        # Prepare cell
        cell = shuffle(
            rotate(MCL(conv_a, conv_b, conv_c, conv_alpha), r1, r2, r3),
            order,
        )
        if is_reasonable(cell):
            prim_a = conv_a
            prim_b, prim_c = sorted([conv_b, conv_c])
            prim_beta = 90.0
            if conv_alpha > 90.0:
                prim_alpha = 180.0 - conv_alpha
            else:
                prim_alpha = conv_alpha
            prim_gamma = 90.0
            old_det = np.linalg.det(cell)

            # Fix cell
            try:
                S = _MCL_get_S_matrix(cell, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            except StandardizationTypeMismatch:
                return
            cell = np.linalg.inv(S.T) @ cell

            # Check results
            a, b, c, alpha, beta, gamma = params(cell)
            assert np.allclose(
                [a, b, c], [prim_a, prim_b, prim_c], rtol=EPS_RELATIVE, atol=EPS_LENGTH
            )
            assert np.allclose(alpha, prim_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE)
            assert np.allclose(beta, prim_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE)
            assert np.allclose(gamma, prim_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE)

            # Check that chirality is the same
            assert np.linalg.det(cell) * old_det > 0


################################################################################
#                                     MCLC                                     #
################################################################################
@example(
    r1=0.0,
    r2=0.0,
    r3=1.0,
    conv_a=1.0,
    conv_b=0.5,
    conv_c=0.0078125,
    conv_alpha=1.0,
    order=2,
)
@given(
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=MIN_ANGLE, max_value=180.0 - MIN_ANGLE),
    st.integers(min_value=0, max_value=n_order),
)
def test_MCLC_get_S_matrix(r1, r2, r3, conv_a, conv_b, conv_c, conv_alpha, order):
    if not np.allclose([r1, r2, r3], [0, 0, 0], rtol=EPS_RELATIVE, atol=EPS_LENGTH):
        # Prepare cell
        cell = shuffle(
            rotate(MCLC(conv_a, conv_b, conv_c, conv_alpha), r1, r2, r3),
            order,
        )
        if is_reasonable(cell):

            conv_b, conv_c = sorted([conv_b, conv_c])
            if conv_alpha > 90.0:
                conv_alpha = 180.0 - conv_alpha

            prim_a = sqrt(conv_a**2 + conv_b**2) / 2
            prim_b = sqrt(conv_a**2 + conv_b**2) / 2
            prim_c = conv_c
            prim_alpha = (
                acos(
                    conv_b
                    * conv_c
                    * cos(conv_alpha * TORADIANS)
                    / 2.0
                    / prim_b
                    / prim_c
                )
                * TODEGREES
            )
            prim_alpha_twin = 180.0 - prim_alpha
            prim_beta = (
                acos(
                    conv_b
                    * conv_c
                    * cos(conv_alpha * TORADIANS)
                    / 2.0
                    / prim_a
                    / prim_c
                )
                * TODEGREES
            )
            prim_beta_twin = 180.0 - prim_beta
            prim_gamma = (
                acos((conv_b**2 - conv_a**2) / 4.0 / prim_a / prim_b) * TODEGREES
            )
            old_det = np.linalg.det(cell)

            # Fix cell
            try:
                S = _MCLC_get_S_matrix(cell, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            except StandardizationTypeMismatch:
                return
            cell = np.linalg.inv(S.T) @ cell

            # Check results
            a, b, c, alpha, beta, gamma = params(cell)
            assert np.allclose(
                [a, b, c], [prim_a, prim_b, prim_c], rtol=EPS_RELATIVE, atol=EPS_LENGTH
            )

            assert (
                compare_numerically(
                    alpha, "==", prim_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    alpha, "==", prim_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    alpha, "==", prim_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    alpha, "==", 180.0 - prim_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    alpha, "==", 180.0 - prim_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    alpha, "==", 180.0 - prim_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
            )
            assert (
                compare_numerically(
                    beta, "==", prim_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    beta, "==", prim_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    beta, "==", prim_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    beta, "==", 180.0 - prim_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    beta, "==", 180.0 - prim_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    beta, "==", 180.0 - prim_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
            )
            assert (
                compare_numerically(
                    gamma, "==", prim_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    gamma, "==", prim_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    gamma, "==", prim_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    gamma, "==", 180.0 - prim_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    gamma, "==", 180.0 - prim_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    gamma, "==", 180.0 - prim_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
            )

            # Check that chirality is the same
            assert np.linalg.det(cell) * old_det > 0


################################################################################
#                                     TRI                                      #
################################################################################
@example(
    r1=0.0,
    r2=0.0,
    r3=1.0,
    a=1.0,
    b=1.0,
    c=1.0,
    alpha=1.0,
    beta=1.0,
    gamma=1.0,
    order=3,
)
@example(
    r1=0.0,  # or any other generated value
    r2=0.0,  # or any other generated value
    r3=1.0,
    a=1111674.0,
    b=1481154.0,
    c=149.0,
    alpha=1.0,
    beta=1.0,
    gamma=1.5,
    order=0,  # or any other generated value
)
@given(
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=MIN_ANGLE, max_value=180.0 - MIN_ANGLE),
    st.floats(min_value=MIN_ANGLE, max_value=180.0 - MIN_ANGLE),
    st.floats(min_value=MIN_ANGLE, max_value=180.0 - MIN_ANGLE),
    st.integers(min_value=0, max_value=n_order),
)
def test_TRI_get_S_matrix(r1, r2, r3, a, b, c, alpha, beta, gamma, order):
    if not np.allclose(
        [r1, r2, r3], [0, 0, 0], rtol=EPS_RELATIVE, atol=EPS_LENGTH
    ) and parallelepiped_check(a, b, c, alpha, beta, gamma):
        # Prepare cell
        cell = shuffle(
            rotate(TRI(a, b, c, alpha, beta, gamma), r1, r2, r3),
            order,
        )
        if is_reasonable(cell):
            prev_cell = cell
            prev_rcell = get_reciprocal(cell)

            k_a, k_b, k_c, k_alpha, k_beta, k_gamma = params(get_reciprocal(cell))
            old_det = np.linalg.det(cell)

            # Fix cell
            try:
                S = _TRI_get_S_matrix(cell, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            except StandardizationTypeMismatch:
                return
            cell = np.linalg.inv(S.T) @ cell

            s_a, s_b, s_c, s_alpha, s_beta, s_gamma = params(cell)
            s_k_a, s_k_b, s_k_c, s_k_alpha, s_k_beta, s_k_gamma = params(
                get_reciprocal(cell)
            )

            # Check that the cell is standardized
            if np.allclose(s_k_gamma, 90, rtol=EPS_RELATIVE, atol=EPS_ANGLE):
                assert (
                    compare_numerically(
                        s_k_alpha, "<=", 90, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                    )
                    and compare_numerically(
                        s_k_beta, "<=", 90, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                    )
                    or compare_numerically(
                        s_k_alpha, ">=", 90, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                    )
                    and compare_numerically(
                        s_k_beta, ">=", 90, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                    )
                )
            else:
                assert (
                    compare_numerically(
                        s_k_alpha, "<=", 90, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                    )
                    and compare_numerically(
                        s_k_beta, "<=", 90, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                    )
                    and compare_numerically(
                        s_k_gamma, "<=", 90, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                    )
                    or compare_numerically(
                        s_k_alpha, ">=", 90, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                    )
                    and compare_numerically(
                        s_k_beta, ">=", 90, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                    )
                    and compare_numerically(
                        s_k_gamma, ">=", 90, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                    )
                )

            # Check that parameters and angles are the same
            assert (
                compare_numerically(a, "==", s_a, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
                or compare_numerically(a, "==", s_b, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
                or compare_numerically(a, "==", s_c, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            )
            assert (
                compare_numerically(b, "==", s_a, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
                or compare_numerically(b, "==", s_b, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
                or compare_numerically(b, "==", s_c, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            )
            assert (
                compare_numerically(c, "==", s_a, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
                or compare_numerically(c, "==", s_b, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
                or compare_numerically(c, "==", s_c, rtol=EPS_RELATIVE, atol=EPS_LENGTH)
            )
            assert (
                compare_numerically(
                    alpha, "==", s_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    alpha, "==", s_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    alpha, "==", s_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    alpha, "==", 180.0 - s_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    alpha, "==", 180.0 - s_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    alpha, "==", 180.0 - s_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
            )
            assert (
                compare_numerically(
                    beta, "==", s_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    beta, "==", s_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    beta, "==", s_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    beta, "==", 180.0 - s_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    beta, "==", 180.0 - s_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    beta, "==", 180.0 - s_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
            )
            assert (
                compare_numerically(
                    gamma, "==", s_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    gamma, "==", s_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    gamma, "==", s_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    gamma, "==", 180.0 - s_alpha, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    gamma, "==", 180.0 - s_beta, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
                or compare_numerically(
                    gamma, "==", 180.0 - s_gamma, rtol=EPS_RELATIVE, atol=EPS_ANGLE
                )
            )

            # Check that the volume is the same
            # The chirality might break here, since we ordering a reciprocal lattice and not the real-space one
            assert compare_numerically(
                np.abs(np.linalg.det(cell)),
                "==",
                np.abs(old_det),
                rtol=EPS_RELATIVE,
                atol=EPS_LENGTH,
            )
            # assert np.linalg.det(cell) * old_det > 0
