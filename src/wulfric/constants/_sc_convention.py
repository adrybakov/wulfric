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
    "cP": np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
    "cF": np.array([[-1.0, 1.0, 1.0], [1.0, -1.0, 1.0], [1.0, 1.0, -1.0]]),
    "cI": np.array([[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]]),
    "tP": np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
    "tI": np.array([[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]]),
    "oP": np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
    "oF": np.array([[-1.0, 1.0, 1.0], [1.0, -1.0, 1.0], [1.0, 1.0, -1.0]]),
    "oI": np.array([[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]]),
    "oA": np.array([[1.0, -1.0, 0], [1.0, 1.0, 0], [0, 0, 1.0]]),
    "oC": np.array([[1.0, -1.0, 0], [1.0, 1.0, 0], [0, 0, 1.0]]),
    "hP": np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
    "hR": np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
    "mP": np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
    "mC": np.array([[1.0, 1.0, 0.0], [-1.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
    "aP": np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
}

SC_BRAVAIS_LATTICE_VARIATIONS = [
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
]

SC_DEFAULT_K_PATHS = {
    "CUB": "G-X-M-G-R-X|M-R",
    "FCC": "G-X-W-K-G-L-U-W-L-K|U-X",
    "BCC": "G-H-N-G-P-H|P-N",
    "TET": "G-X-M-G-Z-R-A-Z|X-R|M-A",
    "BCT1": "G-X-M-G-Z-P-N-Z1-M|X-P",
    "BCT2": "G-X-Y-S-G-Z-S1-N-P-Y1-Z|X-P",
    "ORC": "G-X-S-Y-G-Z-U-R-T-Z|Y-T|U-X|S-R",
    "ORCF1": "G-Y-T-Z-G-X-A1-Y|T-X1|X-A-Z|L-G",
    "ORCF2": "G-Y-C-D-X-G-Z-D1-H-C|C1-Z|X-H1|H-Y|L-G",
    "ORCF3": "G-Y-T-Z-G-X-A1-Y|X-A-Z|L-G",
    "ORCI": "G-X-L-T-W-R-X1-Z-G-Y-S-W|L1-Y|Y1-Z",
    "ORCC": "G-X-S-R-A-Z-G-Y-X1-A1-T-Y|Z-T",
    "HEX": "G-M-K-G-A-L-H-A|L-M|K-H",
    "RHL1": "G-L-B1|B-Z-G-X|Q-F-P1-Z|L-P",
    "RHL2": "G-P-Z-Q-G-F-P1-Q1-L-Z",
    "MCL": "G-Y-H-C-E-M1-A-X-H1|M-D-Z|Y-D",
    "MCLC1": "G-Y-F-L-I|I1-Z-F1|Y-X1|X-G-N|M-G",
    "MCLC2": "G-Y-F-L-I|I1-Z-F1|N-G-M",
    "MCLC3": "G-Y-F-H-Z-I-F1|H1-Y1-X-G-N|M-G",
    "MCLC4": "G-Y-F-H-Z-I|H1-Y1-X-G-N|M-G",
    "MCLC5": "G-Y-F-L-I|I1-Z-H-F1|H1-Y1-X-G-N|M-G",
    "TRI1A": "X-G-Y|L-G-Z|N-G-M|R-G",
    "TRI1B": "X-G-Y|L-G-Z|N-G-M|R-G",
    "TRI2A": "X-G-Y|L-G-Z|N-G-M|R-G",
    "TRI2B": "X-G-Y|L-G-Z|N-G-M|R-G",
}

HS_PLOT_NAMES = {
    "G": "$\\Gamma$",
    "M": "M",
    "R": "R",
    "X": "X",
    "K": "K",
    "L": "L",
    "U": "U",
    "W": "W",
    "H": "H",
    "P": "P",
    "N": "N",
    "A": "A",
    "Z": "Z",
    "Z1": "Z$_1$",
    "Y": "Y",
    "Y1": "Y$_1$",
    "S": "S",  # it is overwritten to sigma if needed.
    "S1": "S$_1$",  # it is overwritten to sigma if needed.
    "T": "T",
    "A1": "A$_1$",
    "X1": "X$_1$",
    "C": "C",
    "C1": "C$_1$",
    "D": "D",
    "D1": "D$_1$",
    "H1": "H$_1$",
    "L1": "L$_1$",
    "L2": "L$_2$",
    "B": "B",
    "B1": "B$_1$",
    "F": "F",
    "P1": "P$_1$",
    "P2": "P$_2$",
    "Q": "Q",
    "Q1": "Q$_1$",
    "E": "E",
    "H2": "H$_2$",
    "M1": "M$_1$",
    "M2": "M$_2$",
    "N1": "N$_1$",
    "F1": "F$_1$",
    "F2": "F$_2$",
    "F3": "F$_3$",
    "I": "I",
    "I1": "I$_1$",
    "X2": "X$_2$",
    "Y2": "Y$_2$",
    "Y3": "Y$_3$",
}


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
