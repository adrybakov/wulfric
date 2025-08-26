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
import numpy as np

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")

################################################################################
#                Hinuma, Pizzi, Kumagai, Oba, Tanaka convention                #
################################################################################


HPKOT_CONVENTIONAL_TO_PRIMITIVE = {
    "cP": np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    ),
    "cF": np.array(
        [
            [0.0, 0.5, 0.5],
            [0.5, 0.0, 0.5],
            [0.5, 0.5, 0.0],
        ]
    ),
    "cI": np.array(
        [
            [-0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, -0.5],
        ]
    ),
    "tP": np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    ),
    "tI": np.array(
        [
            [-0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, -0.5],
        ]
    ),
    "oP": np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    ),
    "oF": np.array(
        [
            [0.0, 0.5, 0.5],
            [0.5, 0.0, 0.5],
            [0.5, 0.5, 0.0],
        ]
    ),
    "oI": np.array(
        [
            [-0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, -0.5],
        ]
    ),
    "oA": np.array(
        [
            [0.0, 0.0, 1.0],
            [0.5, 0.5, 0.0],
            [-0.5, 0.5, 0.0],
        ]
    ),
    "oC": np.array(
        [
            [0.5, 0.5, 0.0],
            [-0.5, 0.5, 0.0],
            [0.0, 0.0, 1.0],
        ]
    ),
    "hP": np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    ),
    "hR": np.array(
        [
            [1.0, -0.5, -0.5],
            [0.5, 0.5, -1.0],
            [0.5, 0.5, 0.5],
        ]
    ),
    "mP": np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    ),
    "mC": np.array(
        [
            [0.5, -0.5, 0.0],
            [0.5, 0.5, 0.0],
            [0.0, 0.0, 1.0],
        ]
    ),
    "aP": np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    ),
}

HPKOT_DEFAULT_K_PATHS = {
    "cP1": "G-X-M-G-R-X|R-M-X1",
    "cP2": "G-X-M-G-R-X|R-M",
    "cF1": "G-X-U|K-G-L-W-X-W2",
    "cF2": "G-X-U|K-G-L-W-X",
    "cI1": "G-H-N-G-P-H|P-N",
    "tP1": "G-X-M-G-Z-R-A-Z|X-R|M-A",
    "tI1": "G-X-M-G-Z|Z0-M|X-P-N-G",
    "tI2": "G-X-P-N-G-M-S|S0-G|X-R|G-M",
    "oP1": "G-X-S-Y-G-Z-U-R-T-Z|X-U|Y-T|S-R",
    "oF1": "G-Y-T-Z-G-SIGMA0|U0-T|Y-C0|A0-Z|G-L",
    "oF2": "G-T-Z-Y-G-LAMBDA0|Q0-Z|T-G0|H0-Y|G-L",
    "oF3": "G-Y-C0|A0-Z-B0|D0-T-G0|H0-Y|T-G-Z|G-L",
    "oI1": "G-X-F2|SIGMA0-G-Y0|U0-X|G-R-W-S-G-T-W",
    "oI2": "G-X-U2|Y0-G-LAMBDA0|G2-X|G-R-W-S-G-T-W",
    "oI3": "G-X-F0|SIGMA0-G-LAMBDA0|G0-X|G-R-W-S-G-T-W",
    "oC1": "G-Y-C0|SIGMA0-G-Z-A0|E0-T-Y|G-S-R-Z-T",
    "oC2": "G-Y-F0|DELTA0-G-Z-B0|G0-T-Y|G-S-R-Z-T",
    "oA1": "G-Y-C0|SIGMA0-G-Z-A0|E0-T-Y|G-S-R-Z-T",
    "oA2": "G-Y-F0|DELTA0-G-Z-B0|G0-T-Y|G-S-R-Z-T",
    "hP1": "G-M-K-G-A-L-H-A|L-M|H-K-H2",
    "hP2": "G-M-K-G-A-L-H-A|L-M|H-K",
    "hR1": "G-T-H2|H0-L-G-S0|S2-F-G",
    "hR2": "G-L-T-P0|P2-G-F",
    "mP1": "G-Z-D-B-G-A-E-Z-C2-Y2-G",
    "mC1": "G-C|C2-Y2-G-M2-D|D2-A-G|L2-G-V2",
    "mC2": "G-Y-M-A-G|L2-G-V2",
    "mC3": "G-A-I2|I-M2-G-Y|L2-G-V2",
    "aP2": "G-X|Y-G-Z|R-G-T|U-G-V",
    "aP3": "G-X|Y-G-Z|R2-G-T2|U2-G-V2",
}

# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
