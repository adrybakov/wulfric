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
    "cP1": "GAMMA-X-M-GAMMA-R-X|R-M-X1",
    "cP2": "GAMMA-X-M-GAMMA-R-X|R-M",
    "cF1": "GAMMA-X-U|K-GAMMA-L-W-X-W2",
    "cF2": "GAMMA-X-U|K-GAMMA-L-W-X",
    "cI1": "GAMMA-H-N-GAMMA-P-H|P-N",
    "tP1": "GAMMA-X-M-GAMMA-Z-R-A-Z|X-R|M-A",
    "tI1": "GAMMA-X-M-GAMMA-Z|Z0-M|X-P-N-GAMMA",
    "tI2": "GAMMA-X-P-N-GAMMA-M-S|S0-GAMMA|X-R|G-M",
    "oP1": "GAMMA-X-S-Y-GAMMA-Z-U-R-T-Z|X-U|Y-T|S-R",
    "oF1": "GAMMA-Y-T-Z-GAMMA-SIGMA0|U0-T|Y-C0|A0-Z|GAMMA-L",
    "oF2": "GAMMA-T-Z-Y-GAMMA-LAMBDA0|Q0-Z|T-G0|H0-Y|GAMMA-L",
    "oF3": "GAMMA-Y-C0|A0-Z-B0|D0-T-G0|H0-Y|T-GAMMA-Z|GAMMA-L",
    "oI1": "GAMMA-X-F2|SIGMA0-GAMMA-Y0|U0-X|GAMMA-R-W-S-GAMMA-T-W",
    "oI2": "GAMMA-X-U2|Y0-GAMMA-LAMBDA0|G2-X|GAMMA-R-W-S-GAMMA-T-W",
    "oI3": "GAMMA-X-F0|SIGMA0-GAMMA-LAMBDA0|G0-X|GAMMA-R-W-S-GAMMA-T-W",
    "oC1": "GAMMA-Y-C0|SIGMA0-GAMMA-Z-A0|E0-T-Y|GAMMA-S-R-Z-T",
    "oC2": "GAMMA-Y-F0|DELTA0-GAMMA-Z-B0|G0-T-Y|GAMMA-S-R-Z-T",
    "oA1": "GAMMA-Y-C0|SIGMA0-GAMMA-Z-A0|E0-T-Y|GAMMA-S-R-Z-T",
    "oA2": "GAMMA-Y-F0|DELTA0-GAMMA-Z-B0|G0-T-Y|GAMMA-S-R-Z-T",
    "hP1": "GAMMA-M-K-GAMMA-A-L-H-A|L-M|H-K-H2",
    "hP2": "GAMMA-M-K-GAMMA-A-L-H-A|L-M|H-K",
    "hR1": "GAMMA-T-H2|H0-L-GAMMA-S0|S2-F-GAMMA",
    "hR2": "GAMMA-L-T-P0|P2-GAMMA-F",
    "mP1": "GAMMA-Z-D-B-GAMMA-A-E-Z-C2-Y2-GAMMA",
    "mC1": "GAMMA-C|C2-Y2-GAMMA-M2-D|D2-A-GAMMA|L2-GAMMA-V2",
    "mC2": "GAMMA-Y-M-A-GAMMA|L2-GAMMA-V2",
    "mC3": "GAMMA-A-I2|I-M2-GAMMA-Y|L2-GAMMA-V2",
    "aP2": "GAMMA-X|Y-GAMMA-Z|R-GAMMA-T|U-GAMMA-V",
    "aP3": "GAMMA-X|Y-GAMMA-Z|R2-GAMMA-T2|U2-GAMMA-V2",
}

# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
