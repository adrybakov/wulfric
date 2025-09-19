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
#                      Setyawan and Curtarolo conventions                      #
################################################################################

SC_BRAVAIS_LATTICE_SHORT_NAMES = {
    "cP": "CUB",
    "cF": "FCC",
    "cI": "BCC",
    "tP": "TET",
    "tI": "BCT",
    "oP": "ORC",
    "oF": "ORCF",
    "oI": "ORCI",
    "oA": "ORCC",
    "oC": "ORCC",
    "hP": "HEX",
    "hR": "RHL",
    "mP": "MCL",
    "mC": "MCLC",
    "aP": "TRI",
}

SC_BRAVAIS_LATTICE_LONG_NAMES = {
    "cP": "Cubic",
    "cF": "Face-centered cubic",
    "cI": "Body-centered cubic",
    "tP": "Tetragonal",
    "tI": "Body-centered tetragonal",
    "oP": "Orthorhombic",
    "oF": "Face-centered orthorhombic",
    "oI": "Body-centered orthorhombic",
    "oA": "C-centered orthorhombic",
    "oC": "C-centered orthorhombic",
    "hP": "Hexagonal",
    "hR": "Rhombohedral",
    "mP": "Monoclinic",
    "mC": "C-centered monoclinic",
    "aP": "Triclinic",
}

SC_CONVENTIONAL_TO_PRIMITIVE = {
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
            [0.5, 0.5, 0.0],
            [-0.5, 0.5, 0.0],
            [0.0, 0.0, 1.0],
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
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
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

SC_BRAVAIS_LATTICE_VARIATIONS = (
    "CUB",
    "FCC",
    "BCC",
    "TET",
    "BCT1",
    "BCT2",
    "ORC",
    "ORCF1",
    "ORCF2",
    "ORCF3",
    "ORCI",
    "ORCC",
    "HEX",
    "RHL1",
    "RHL2",
    "MCL",
    "MCLC1",
    "MCLC2",
    "MCLC3",
    "MCLC4",
    "MCLC5",
    "TRI1a",
    "TRI2a",
    "TRI1b",
    "TRI2b",
)

SC_DEFAULT_K_PATHS = {
    "CUB": "GAMMA-X-M-GAMMA-R-X|M-R",
    "FCC": "GAMMA-X-W-K-GAMMA-L-U-W-L-K|U-X",
    "BCC": "GAMMA-H-N-GAMMA-P-H|P-N",
    "TET": "GAMMA-X-M-GAMMA-Z-R-A-Z|X-R|M-A",
    "BCT1": "GAMMA-X-M-GAMMA-Z-P-N-Z1-M|X-P",
    "BCT2": "GAMMA-X-Y-SIGMA-GAMMA-Z-SIGMA1-N-P-Y1-Z|X-P",
    "ORC": "GAMMA-X-S-Y-GAMMA-Z-U-R-T-Z|Y-T|U-X|S-R",
    "ORCF1": "GAMMA-Y-T-Z-GAMMA-X-A1-Y|T-X1|X-A-Z|L-GAMMA",
    "ORCF2": "GAMMA-Y-C-D-X-GAMMA-Z-D1-H-C|C1-Z|X-H1|H-Y|L-GAMMA",
    "ORCF3": "GAMMA-Y-T-Z-GAMMA-X-A1-Y|X-A-Z|L-GAMMA",
    "ORCI": "GAMMA-X-L-T-W-R-X1-Z-GAMMA-Y-S-W|L1-Y|Y1-Z",
    "ORCC": "GAMMA-X-S-R-A-Z-GAMMA-Y-X1-A1-T-Y|Z-T",
    "HEX": "GAMMA-M-K-GAMMA-A-L-H-A|L-M|K-H",
    "RHL1": "GAMMA-L-B1|B-Z-GAMMA-X|Q-F-P1-Z|L-P",
    "RHL2": "GAMMA-P-Z-Q-GAMMA-F-P1-Q1-L-Z",
    "MCL": "GAMMA-Y-H-C-E-M1-A-X-H1|M-D-Z|Y-D",
    "MCLC1": "GAMMA-Y-F-L-I|I1-Z-F1|Y-X1|X-GAMMA-N|M-GAMMA",
    "MCLC2": "GAMMA-Y-F-L-I|I1-Z-F1|N-GAMMA-M",
    "MCLC3": "GAMMA-Y-F-H-Z-I-F1|H1-Y1-X-GAMMA-N|M-GAMMA",
    "MCLC4": "GAMMA-Y-F-H-Z-I|H1-Y1-X-GAMMA-N|M-GAMMA",
    "MCLC5": "GAMMA-Y-F-L-I|I1-Z-H-F1|H1-Y1-X-GAMMA-N|M-GAMMA",
    "TRI1a": "X-GAMMA-Y|L-GAMMA-Z|N-GAMMA-M|R-GAMMA",
    "TRI2a": "X-GAMMA-Y|L-GAMMA-Z|N-GAMMA-M|R-GAMMA",
    "TRI1b": "X-GAMMA-Y|L-GAMMA-Z|N-GAMMA-M|R-GAMMA",
    "TRI2b": "X-GAMMA-Y|L-GAMMA-Z|N-GAMMA-M|R-GAMMA",
}


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
