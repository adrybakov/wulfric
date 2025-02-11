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
import pytest
from hypothesis import example, given
from hypothesis import strategies as st

from wulfric._exceptions import StandardizationTypeMismatch
from wulfric._numerical import compare_numerically
from wulfric.cell._basic_manipulation import get_params, get_reciprocal, is_reasonable
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
from wulfric.constants._numerical import TODEGREES, TORADIANS
from wulfric.geometry._geometry import parallelepiped_check

# General note
# The random rotation have been removed from the tests, as it invited a lot of problems
# with the float point arithmetics.
# In the future the tests might be improved with a new formally described testing protocol.

################################################################################
#                               Service routines                               #
################################################################################
ANGLE_TOLERANCE = 1e-4
LENGTH_TOLERANCE = 1e-8
MIN_LENGTH = 1e-7
MAX_LENGTH = 1e7

ORDERS = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]

MAX_COMBINATIONS = 48


def shuffle(cell, combination):
    i = 0
    for first, second, third in ORDERS:
        for f_pm in [-1, 1]:
            for s_pm in [-1, 1]:
                for t_pm in [-1, 1]:
                    a_1 = f_pm * cell[first]
                    a_2 = s_pm * cell[second]
                    a_3 = t_pm * cell[third]
                    if i == combination:
                        break

    return [a_1, a_2, a_3]


# ################################################################################
# #                                      CUB                                     #
# ################################################################################
# @pytest.mark.parametrize("combination", range(1, 49))
# @given(conv_a=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH))
# def test_CUB_get_S_matrix(conv_a, combination):

#     # Prepare cell
#     cell = shuffle(CUB(conv_a), combination)

#     angle = 90.0
#     old_det = np.linalg.det(cell)

#     # Fix cell
#     S = _CUB_get_S_matrix(cell)
#     cell = S.T @ cell

#     # Check results
#     a, b, c, alpha, beta, gamma = get_params(cell)
#     assert compare_numerically(a, "==", conv_a, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(b, "==", conv_a, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(c, "==", conv_a, eps=LENGTH_TOLERANCE)

#     assert compare_numerically(alpha, "==", angle, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(beta, "==", angle, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(gamma, "==", angle, eps=ANGLE_TOLERANCE)

#     # Check that chirality is the same
#     assert np.linalg.det(cell) * old_det > 0


# ################################################################################
# #                                      FCC                                     #
# ################################################################################
# @pytest.mark.parametrize("combination", range(1, 49))
# @given(conv_a=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH))
# def test_FCC_get_S_matrix(conv_a, combination):

#     # Prepare cell
#     cell = shuffle(FCC(conv_a), combination)

#     prim_a = conv_a * sqrt(2.0) / 2.0
#     angle = 60.0
#     old_det = np.linalg.det(cell)

#     # Fix cell
#     S = _FCC_get_S_matrix(cell)
#     cell = S.T @ cell

#     # Check results
#     a, b, c, alpha, beta, gamma = get_params(cell)
#     assert compare_numerically(a, "==", prim_a, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(b, "==", prim_a, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(c, "==", prim_a, eps=LENGTH_TOLERANCE)

#     assert compare_numerically(alpha, "==", angle, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(beta, "==", angle, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(gamma, "==", angle, eps=ANGLE_TOLERANCE)

#     # Check that chirality is the same
#     assert np.linalg.det(cell) * old_det > 0


# ################################################################################
# #                                      BCC                                     #
# ################################################################################
# @pytest.mark.parametrize("combination", range(1, 49))
# @given(conv_a=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH))
# def test_BCC_get_S_matrix(conv_a, combination):

#     # Prepare cell
#     cell = shuffle(BCC(conv_a), combination)

#     angle = acos(-1 / 3) * TODEGREES
#     prim_a = conv_a * sqrt(3) / 2
#     old_det = np.linalg.det(cell)

#     # Fix cell
#     S = _BCC_get_S_matrix(cell)
#     cell = S.T @ cell

#     # Check results
#     a, b, c, alpha, beta, gamma = get_params(cell)
#     assert compare_numerically(a, "==", prim_a, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(b, "==", prim_a, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(c, "==", prim_a, eps=LENGTH_TOLERANCE)

#     assert compare_numerically(alpha, "==", angle, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(beta, "==", angle, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(gamma, "==", angle, eps=ANGLE_TOLERANCE)

#     # Check that chirality is the same
#     assert np.linalg.det(cell) * old_det > 0


# ################################################################################
# #                                      TET                                     #
# ################################################################################
# @pytest.mark.parametrize("combination", range(1, 49))
# @given(
#     conv_a=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_c=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
# )
# def test_TET_get_S_matrix(conv_a, conv_c, combination):

#     # Prepare cell
#     cell = shuffle(TET(conv_a, conv_c), combination)

#     angle = 90.0
#     prim_a = conv_a
#     prim_c = conv_c
#     old_det = np.linalg.det(cell)

#     # Fix cell
#     try:
#         S = _TET_get_S_matrix(cell)
#     except StandardizationTypeMismatch:
#         return
#     cell = S.T @ cell

#     # Check results
#     a, b, c, alpha, beta, gamma = get_params(cell)
#     assert compare_numerically(a, "==", prim_a, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(b, "==", prim_a, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(c, "==", prim_c, eps=LENGTH_TOLERANCE)

#     assert compare_numerically(alpha, "==", angle, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(beta, "==", angle, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(gamma, "==", angle, eps=ANGLE_TOLERANCE)

#     # Check that chirality is the same
#     assert np.linalg.det(cell) * old_det > 0


# ################################################################################
# #                                      BCT                                     #
# ################################################################################
# @pytest.mark.parametrize("combination", range(1, 49))
# @given(
#     conv_a=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_c=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
# )
# def test_BCT_get_S_matrix(conv_a, conv_c, combination):

#     # Prepare cell
#     cell = shuffle(BCT(conv_a, conv_c), combination)

#     prim = sqrt(2 * conv_a**2 + conv_c**2) / 2
#     angle12 = (
#         acos(np.clip((conv_c**2 - 2 * conv_a**2) / 4 / prim**2, -1, 1)) * TODEGREES
#     )
#     angle = acos(np.clip(-(conv_c**2) / 4 / prim**2, -1, 1)) * TODEGREES

#     old_det = np.linalg.det(cell)

#     # Fix cell
#     try:
#         S = _BCT_get_S_matrix(cell)
#     except StandardizationTypeMismatch:
#         return
#     cell = S.T @ cell

#     # Check results
#     a, b, c, alpha, beta, gamma = get_params(cell)
#     assert compare_numerically(a, "==", prim, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(b, "==", prim, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(c, "==", prim, eps=LENGTH_TOLERANCE)

#     assert compare_numerically(alpha, "==", angle, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(beta, "==", angle, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(gamma, "==", angle12, eps=ANGLE_TOLERANCE)

#     # Check that chirality is the same
#     assert np.linalg.det(cell) * old_det > 0


# ################################################################################
# #                                      ORC                                     #
# ################################################################################
# @pytest.mark.parametrize("combination", range(1, 49))
# @given(
#     conv_a=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_b=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_c=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
# )
# def test_ORC_get_S_matrix(conv_a, conv_b, conv_c, combination):

#     # Prepare cell
#     cell = shuffle(ORC(conv_a, conv_b, conv_c), combination)

#     prim_a, prim_b, prim_c = sorted([conv_a, conv_b, conv_c])
#     angle = 90.0

#     old_det = np.linalg.det(cell)

#     # Fix cell
#     try:
#         S = _ORC_get_S_matrix(cell)
#     except StandardizationTypeMismatch:
#         return
#     cell = S.T @ cell

#     # Check results
#     a, b, c, alpha, beta, gamma = get_params(cell)
#     assert compare_numerically(a, "==", prim_a, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(b, "==", prim_b, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(c, "==", prim_c, eps=LENGTH_TOLERANCE)

#     assert compare_numerically(alpha, "==", angle, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(beta, "==", angle, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(gamma, "==", angle, eps=ANGLE_TOLERANCE)

#     # Check that chirality is the same
#     assert np.linalg.det(cell) * old_det > 0


# ################################################################################
# #                                     ORCF                                     #
# ################################################################################
# @pytest.mark.parametrize("combination", range(1, 49))
# @given(
#     conv_a=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_b=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_c=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
# )
# def test_ORCF_get_S_matrix(conv_a, conv_b, conv_c, combination):

#     # Prepare cell
#     cell = shuffle(ORCF(conv_a, conv_b, conv_c), combination)

#     conv_a, conv_b, conv_c = sorted([conv_a, conv_b, conv_c])
#     prim_a = sqrt(conv_b**2 + conv_c**2) / 2.0
#     prim_b = sqrt(conv_a**2 + conv_c**2) / 2.0
#     prim_c = sqrt(conv_a**2 + conv_b**2) / 2.0
#     prim_alpha = acos(np.clip(conv_a**2 / 4.0 / prim_b / prim_c, -1, 1)) * TODEGREES
#     prim_alpha_twin = 180.0 - prim_alpha
#     prim_beta = acos(np.clip(conv_b**2 / 4.0 / prim_a / prim_c, -1, 1)) * TODEGREES
#     prim_beta_twin = 180.0 - prim_beta
#     prim_gamma = acos(np.clip(conv_c**2 / 4.0 / prim_a / prim_b, -1, 1)) * TODEGREES
#     prim_gamma_twin = 180.0 - prim_gamma
#     old_det = np.linalg.det(cell)

#     # Fix cell
#     try:
#         S = _ORCF_get_S_matrix(cell)
#     except StandardizationTypeMismatch:
#         return

#     cell = S.T @ cell

#     # Check results
#     a, b, c, alpha, beta, gamma = get_params(cell)
#     assert compare_numerically(a, "==", prim_a, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(b, "==", prim_b, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(c, "==", prim_c, eps=LENGTH_TOLERANCE)

#     assert compare_numerically(
#         alpha, "==", prim_alpha, eps=ANGLE_TOLERANCE
#     ) or compare_numerically(alpha, "==", prim_alpha_twin, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(
#         beta, "==", prim_beta, eps=ANGLE_TOLERANCE
#     ) or compare_numerically(beta, "==", prim_beta_twin, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(
#         gamma, "==", prim_gamma, eps=ANGLE_TOLERANCE
#     ) or compare_numerically(gamma, "==", prim_gamma_twin, eps=ANGLE_TOLERANCE)

#     # Check that chirality is the same
#     assert np.linalg.det(cell) * old_det > 0


# ################################################################################
# #                                     ORCI                                     #
# ################################################################################
# @pytest.mark.parametrize("combination", range(1, 49))
# @given(
#     conv_a=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_b=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_c=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
# )
# def test_ORCI_get_S_matrix(conv_a, conv_b, conv_c, combination):

#     # Prepare cell
#     cell = shuffle(ORCI(conv_a, conv_b, conv_c), combination)

#     conv_a, conv_b, conv_c = sorted([conv_a, conv_b, conv_c])
#     prim = sqrt(conv_a**2 + conv_b**2 + conv_c**2) / 2

#     prim_alpha = (
#         acos(np.clip((conv_a**2 - conv_b**2 - conv_c**2) / 4.0 / prim**2, -1, 1))
#         * TODEGREES
#     )
#     prim_beta = (
#         acos(np.clip((-(conv_a**2) + conv_b**2 - conv_c**2) / 4.0 / prim**2, -1, 1))
#         * TODEGREES
#     )
#     prim_gamma = (
#         acos(np.clip((-(conv_a**2) - conv_b**2 + conv_c**2) / 4.0 / prim**2, -1, 1))
#         * TODEGREES
#     )

#     prim_alpha_twin = 180.0 - prim_alpha
#     prim_beta_twin = 180.0 - prim_beta
#     prim_gamma_twin = 180.0 - prim_gamma

#     old_det = np.linalg.det(cell)

#     # Fix cell
#     try:
#         S = _ORCI_get_S_matrix(cell)
#     except StandardizationTypeMismatch:
#         return
#     cell = S.T @ cell

#     # Check results
#     a, b, c, alpha, beta, gamma = get_params(cell)
#     assert compare_numerically(a, "==", prim, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(b, "==", prim, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(c, "==", prim, eps=LENGTH_TOLERANCE)

#     assert compare_numerically(
#         alpha, "==", prim_alpha, eps=ANGLE_TOLERANCE
#     ) or compare_numerically(alpha, "==", prim_alpha_twin, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(
#         beta, "==", prim_beta, eps=ANGLE_TOLERANCE
#     ) or compare_numerically(beta, "==", prim_beta_twin, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(
#         gamma, "==", prim_gamma, eps=ANGLE_TOLERANCE
#     ) or compare_numerically(gamma, "==", prim_gamma_twin, eps=ANGLE_TOLERANCE)

#     # Check that chirality is the same
#     assert np.linalg.det(cell) * old_det > 0


# ################################################################################
# #                                     ORCC                                     #
# ################################################################################
# @pytest.mark.parametrize("combination", range(1, 49))
# @given(
#     conv_a=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_b=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_c=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
# )
# def test_ORCC_get_S_matrix(conv_a, conv_b, conv_c, combination):

#     # Prepare cell
#     cell = shuffle(ORCC(conv_a, conv_b, conv_c), combination)

#     conv_a, conv_b = sorted([conv_a, conv_b])
#     prim_a = sqrt(conv_a**2 + conv_b**2) / 2
#     prim_b = prim_a
#     prim_c = conv_c
#     prim_alpha = 90.0
#     prim_beta = prim_alpha
#     prim_gamma = (
#         acos(np.clip((conv_a**2 - conv_b**2) / 4.0 / prim_a / prim_b, -1, 1))
#         * TODEGREES
#     )

#     prim_gamma_twin = 180.0 - prim_gamma

#     old_det = np.linalg.det(cell)

#     # Fix the cell
#     try:
#         S = _ORCC_get_S_matrix(cell)
#     except StandardizationTypeMismatch:
#         return
#     cell = S.T @ cell

#     # Check results
#     a, b, c, alpha, beta, gamma = get_params(cell)
#     assert compare_numerically(a, "==", prim_a, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(b, "==", prim_b, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(c, "==", prim_c, eps=LENGTH_TOLERANCE)

#     assert compare_numerically(alpha, "==", prim_alpha, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(beta, "==", prim_beta, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(
#         gamma, "==", prim_gamma, eps=ANGLE_TOLERANCE
#     ) or compare_numerically(gamma, "==", prim_gamma_twin, eps=ANGLE_TOLERANCE)

#     # Check that chirality is the same
#     assert np.linalg.det(cell) * old_det > 0


# ################################################################################
# #                                     HEX                                      #
# ################################################################################
# @pytest.mark.parametrize("combination", range(1, 49))
# @given(
#     conv_a=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_c=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
# )
# def test_HEX_get_S_matrix(conv_a, conv_c, combination):

#     # Prepare cell
#     cell = shuffle(HEX(conv_a, conv_c), combination)

#     prim_a = conv_a
#     prim_b = conv_a
#     prim_c = conv_c
#     prim_alpha = 90.0
#     prim_beta = 90.0
#     prim_gamma = 120.0

#     old_det = np.linalg.det(cell)

#     # Fix cell
#     try:
#         S = _HEX_get_S_matrix(cell)
#     except StandardizationTypeMismatch:
#         return
#     cell = S.T @ cell

#     # Check results
#     a, b, c, alpha, beta, gamma = get_params(cell)
#     assert compare_numerically(a, "==", prim_a, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(b, "==", prim_b, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(c, "==", prim_c, eps=LENGTH_TOLERANCE)

#     assert compare_numerically(alpha, "==", prim_alpha, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(beta, "==", prim_beta, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(gamma, "==", prim_gamma, eps=ANGLE_TOLERANCE)

#     # Check that chirality is the same
#     assert np.linalg.det(cell) * old_det > 0


# ################################################################################
# #                                     RHL                                      #
# ################################################################################
# @pytest.mark.parametrize("combination", range(1, 49))
# @given(
#     conv_a=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_alpha=st.floats(min_value=ANGLE_TOLERANCE, max_value=120.0 - ANGLE_TOLERANCE),
# )
# def test_RHL_get_S_matrix(conv_a, conv_alpha, combination):

#     # Prepare cell
#     cell = shuffle(RHL(conv_a, conv_alpha), combination)

#     prim_a = conv_a
#     prim_b = conv_a
#     prim_c = conv_a
#     prim_alpha = conv_alpha
#     prim_beta = conv_alpha
#     prim_gamma = conv_alpha
#     old_det = np.linalg.det(cell)

#     # Fix cell
#     S = _RHL_get_S_matrix(cell)
#     cell = S.T @ cell

#     # Check results
#     a, b, c, alpha, beta, gamma = get_params(cell)
#     assert compare_numerically(a, "==", prim_a, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(b, "==", prim_b, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(c, "==", prim_c, eps=LENGTH_TOLERANCE)

#     assert compare_numerically(alpha, "==", prim_alpha, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(beta, "==", prim_beta, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(gamma, "==", prim_gamma, eps=ANGLE_TOLERANCE)

#     # Check that chirality is the same
#     assert np.linalg.det(cell) * old_det > 0


# ################################################################################
# #                                     MCL                                      #
# ################################################################################
# @pytest.mark.parametrize("combination", range(1, 49))
# @given(
#     conv_a=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_b=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_c=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_alpha=st.floats(min_value=ANGLE_TOLERANCE, max_value=180.0 - ANGLE_TOLERANCE),
# )
# def test_MCL_get_S_matrix(conv_a, conv_b, conv_c, conv_alpha, combination):

#     # Prepare cell
#     cell = shuffle(MCL(conv_a, conv_b, conv_c, conv_alpha), combination)

#     prim_a = conv_a
#     prim_b, prim_c = sorted([conv_b, conv_c])
#     prim_beta = 90.0
#     if conv_alpha > 90.0:
#         prim_alpha = 180.0 - conv_alpha
#     else:
#         prim_alpha = conv_alpha
#     prim_gamma = 90.0
#     old_det = np.linalg.det(cell)

#     # Fix cell
#     try:
#         S = _MCL_get_S_matrix(cell)
#     except StandardizationTypeMismatch:
#         return
#     cell = S.T @ cell

#     # Check results
#     a, b, c, alpha, beta, gamma = get_params(cell)
#     assert compare_numerically(a, "==", prim_a, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(b, "==", prim_b, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(c, "==", prim_c, eps=LENGTH_TOLERANCE)

#     assert compare_numerically(alpha, "==", prim_alpha, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(beta, "==", prim_beta, eps=ANGLE_TOLERANCE)
#     assert compare_numerically(gamma, "==", prim_gamma, eps=ANGLE_TOLERANCE)

#     # Check that chirality is the same
#     assert np.linalg.det(cell) * old_det > 0


# ################################################################################
# #                                     MCLC                                     #
# ################################################################################
# @pytest.mark.parametrize("combination", range(1, 49))
# @given(
#     conv_a=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_b=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_c=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
#     conv_alpha=st.floats(min_value=ANGLE_TOLERANCE, max_value=180.0 - ANGLE_TOLERANCE),
# )
# def test_MCLC_get_S_matrix(conv_a, conv_b, conv_c, conv_alpha, combination):

#     # Prepare cell
#     cell = shuffle(MCLC(conv_a, conv_b, conv_c, conv_alpha), combination)

#     conv_b, conv_c = sorted([conv_b, conv_c])
#     if conv_alpha > 90.0:
#         conv_alpha = 180.0 - conv_alpha

#     prim_a = sqrt(conv_a**2 + conv_b**2) / 2
#     prim_b = sqrt(conv_a**2 + conv_b**2) / 2
#     prim_c = conv_c
#     prim_alpha = (
#         acos(
#             np.clip(
#                 conv_b * conv_c * cos(conv_alpha * TORADIANS) / 2.0 / prim_b / prim_c,
#                 -1,
#                 1,
#             )
#         )
#         * TODEGREES
#     )
#     prim_alpha_twin = 180.0 - prim_alpha
#     prim_beta = (
#         acos(
#             np.clip(
#                 conv_b * conv_c * cos(conv_alpha * TORADIANS) / 2.0 / prim_a / prim_c,
#                 -1,
#                 1,
#             )
#         )
#         * TODEGREES
#     )
#     prim_beta_twin = 180.0 - prim_beta
#     prim_gamma = (
#         acos(np.clip((conv_b**2 - conv_a**2) / 4.0 / prim_a / prim_b, -1, 1))
#         * TODEGREES
#     )
#     old_det = np.linalg.det(cell)

#     # Fix cell
#     try:
#         S = _MCLC_get_S_matrix(cell)
#     except StandardizationTypeMismatch:
#         return
#     cell = S.T @ cell

#     # Check results
#     a, b, c, alpha, beta, gamma = get_params(cell)
#     assert compare_numerically(a, "==", prim_a, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(b, "==", prim_b, eps=LENGTH_TOLERANCE)
#     assert compare_numerically(c, "==", prim_c, eps=LENGTH_TOLERANCE)

#     assert (
#         compare_numerically(alpha, "==", prim_alpha, eps=ANGLE_TOLERANCE)
#         or compare_numerically(alpha, "==", prim_beta, eps=ANGLE_TOLERANCE)
#         or compare_numerically(alpha, "==", prim_gamma, eps=ANGLE_TOLERANCE)
#         or compare_numerically(alpha, "==", 180.0 - prim_alpha, eps=ANGLE_TOLERANCE)
#         or compare_numerically(alpha, "==", 180.0 - prim_beta, eps=ANGLE_TOLERANCE)
#         or compare_numerically(alpha, "==", 180.0 - prim_gamma, eps=ANGLE_TOLERANCE)
#     )
#     assert (
#         compare_numerically(beta, "==", prim_alpha, eps=ANGLE_TOLERANCE)
#         or compare_numerically(beta, "==", prim_beta, eps=ANGLE_TOLERANCE)
#         or compare_numerically(beta, "==", prim_gamma, eps=ANGLE_TOLERANCE)
#         or compare_numerically(beta, "==", 180.0 - prim_alpha, eps=ANGLE_TOLERANCE)
#         or compare_numerically(beta, "==", 180.0 - prim_beta, eps=ANGLE_TOLERANCE)
#         or compare_numerically(beta, "==", 180.0 - prim_gamma, eps=ANGLE_TOLERANCE)
#     )
#     assert (
#         compare_numerically(gamma, "==", prim_alpha, eps=ANGLE_TOLERANCE)
#         or compare_numerically(gamma, "==", prim_beta, eps=ANGLE_TOLERANCE)
#         or compare_numerically(gamma, "==", prim_gamma, eps=ANGLE_TOLERANCE)
#         or compare_numerically(gamma, "==", 180.0 - prim_alpha, eps=ANGLE_TOLERANCE)
#         or compare_numerically(gamma, "==", 180.0 - prim_beta, eps=ANGLE_TOLERANCE)
#         or compare_numerically(gamma, "==", 180.0 - prim_gamma, eps=ANGLE_TOLERANCE)
#     )

#     # Check that chirality is the same
#     assert np.linalg.det(cell) * old_det > 0


################################################################################
#                                     TRI                                      #
################################################################################
@pytest.mark.parametrize("combination", range(1, 49))
@given(
    a=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
    b=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
    c=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
    alpha=st.floats(min_value=ANGLE_TOLERANCE, max_value=180.0 - ANGLE_TOLERANCE),
    beta=st.floats(min_value=ANGLE_TOLERANCE, max_value=180.0 - ANGLE_TOLERANCE),
    gamma=st.floats(min_value=ANGLE_TOLERANCE, max_value=180.0 - ANGLE_TOLERANCE),
)
def test_TRI_get_S_matrix(a, b, c, alpha, beta, gamma, combination):

    # Check that parameters can form a parallelepiped
    if not parallelepiped_check(a, b, c, alpha, beta, gamma):
        return

    # Prepare cell
    cell = shuffle(TRI(a, b, c, alpha, beta, gamma), combination)

    if np.linalg.det(cell) == 0:
        return

    prev_cell = cell
    prev_rcell = get_reciprocal(cell)

    k_a, k_b, k_c, k_alpha, k_beta, k_gamma = get_params(get_reciprocal(cell))
    old_det = np.linalg.det(cell)

    # Fix cell
    try:
        S = _TRI_get_S_matrix(cell)
    except StandardizationTypeMismatch:
        return
    cell = S.T @ cell

    s_a, s_b, s_c, s_alpha, s_beta, s_gamma = get_params(cell)
    s_k_a, s_k_b, s_k_c, s_k_alpha, s_k_beta, s_k_gamma = get_params(
        get_reciprocal(cell)
    )

    # Check that the cell is standardized
    if np.allclose(s_k_gamma, 90):
        assert (
            compare_numerically(s_k_alpha, "<=", 90, eps=ANGLE_TOLERANCE)
            and compare_numerically(s_k_beta, "<=", 90, eps=ANGLE_TOLERANCE)
            or compare_numerically(s_k_alpha, ">=", 90, eps=ANGLE_TOLERANCE)
            and compare_numerically(s_k_beta, ">=", 90, eps=ANGLE_TOLERANCE)
        )
    else:
        assert (
            compare_numerically(s_k_alpha, "<=", 90, eps=ANGLE_TOLERANCE)
            and compare_numerically(s_k_beta, "<=", 90, eps=ANGLE_TOLERANCE)
            and compare_numerically(s_k_gamma, "<=", 90, eps=ANGLE_TOLERANCE)
            or compare_numerically(s_k_alpha, ">=", 90, eps=ANGLE_TOLERANCE)
            and compare_numerically(s_k_beta, ">=", 90, eps=ANGLE_TOLERANCE)
            and compare_numerically(s_k_gamma, ">=", 90, eps=ANGLE_TOLERANCE)
        )

    # # Check that parameters and angles are the same
    # assert (
    #     compare_numerically(a, "==", s_a, eps=LENGTH_TOLERANCE)
    #     or compare_numerically(a, "==", s_b, eps=LENGTH_TOLERANCE)
    #     or compare_numerically(a, "==", s_c, eps=LENGTH_TOLERANCE)
    # )
    # assert (
    #     compare_numerically(b, "==", s_a, eps=LENGTH_TOLERANCE)
    #     or compare_numerically(b, "==", s_b, eps=LENGTH_TOLERANCE)
    #     or compare_numerically(b, "==", s_c, eps=LENGTH_TOLERANCE)
    # )
    # assert (
    #     compare_numerically(c, "==", s_a, eps=LENGTH_TOLERANCE)
    #     or compare_numerically(c, "==", s_b, eps=LENGTH_TOLERANCE)
    #     or compare_numerically(c, "==", s_c, eps=LENGTH_TOLERANCE)
    # )
    # assert (
    #     compare_numerically(alpha, "==", s_alpha, eps=ANGLE_TOLERANCE)
    #     or compare_numerically(alpha, "==", s_beta, eps=ANGLE_TOLERANCE)
    #     or compare_numerically(alpha, "==", s_gamma, eps=ANGLE_TOLERANCE)
    #     or compare_numerically(alpha, "==", 180.0 - s_alpha, eps=ANGLE_TOLERANCE)
    #     or compare_numerically(alpha, "==", 180.0 - s_beta, eps=ANGLE_TOLERANCE)
    #     or compare_numerically(alpha, "==", 180.0 - s_gamma, eps=ANGLE_TOLERANCE)
    # )
    # assert (
    #     compare_numerically(beta, "==", s_alpha, eps=ANGLE_TOLERANCE)
    #     or compare_numerically(beta, "==", s_beta, eps=ANGLE_TOLERANCE)
    #     or compare_numerically(beta, "==", s_gamma, eps=ANGLE_TOLERANCE)
    #     or compare_numerically(beta, "==", 180.0 - s_alpha, eps=ANGLE_TOLERANCE)
    #     or compare_numerically(beta, "==", 180.0 - s_beta, eps=ANGLE_TOLERANCE)
    #     or compare_numerically(beta, "==", 180.0 - s_gamma, eps=ANGLE_TOLERANCE)
    # )
    # assert (
    #     compare_numerically(gamma, "==", s_alpha, eps=ANGLE_TOLERANCE)
    #     or compare_numerically(gamma, "==", s_beta, eps=ANGLE_TOLERANCE)
    #     or compare_numerically(gamma, "==", s_gamma, eps=ANGLE_TOLERANCE)
    #     or compare_numerically(gamma, "==", 180.0 - s_alpha, eps=ANGLE_TOLERANCE)
    #     or compare_numerically(gamma, "==", 180.0 - s_beta, eps=ANGLE_TOLERANCE)
    #     or compare_numerically(gamma, "==", 180.0 - s_gamma, eps=ANGLE_TOLERANCE)
    # )

    # Check that the volume is the same
    # The chirality might break here, since we ordering a reciprocal lattice and not the real-space one
    assert compare_numerically(np.abs(np.linalg.det(cell)), "==", np.abs(old_det))
    # assert np.linalg.det(cell) * old_det > 0
