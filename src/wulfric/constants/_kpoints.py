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
# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


HS_PLOT_NAMES = {
    "A": "A",
    "A0": "A$_0$",
    "A1": "A$_1$",
    "B": "B",
    "B0": "B$_0$",
    "B1": "B$_1$",
    "C": "C",
    "C0": "C$_0$",
    "C1": "C$_1$",
    "C2": "C$_2$",
    "D": "D",
    "D0": "D$_0$",
    "D1": "D$_1$",
    "D2": "D$_2$",
    "DELTA0": R"$\Delta_0$",
    "E": "E",
    "E0": "E$_0$",
    "F": "F",
    "F0": "F$_0$",
    "F1": "F$_1$",
    "F2": "F$_2$",
    "GAMMA": R"$\Gamma$",
    "G0": "G$_0$",
    "G2": "G$_2$",
    "H": "H",
    "H0": "H$_0$",
    "H1": "H$_1$",
    "H2": "H$_2$",
    "I": "I",
    "I1": "I$_1$",
    "I2": "I$_2$",
    "K": "K",
    "L": "L",
    "L1": "L$_1$",
    "L2": "L$_2$",
    "LAMBDA0": R"$\Lambda_0$",
    "M": "M",
    "M1": "M$_1$",
    "M2": "M$_2$",
    "N": "N",
    "P": "P",
    "P0": "P$_0$",
    "P1": "P$_1$",
    "P2": "P$_2$",
    "Q": "Q",
    "Q0": "Q$_0$",
    "Q1": "Q$_1$",
    "R": "R",
    "R2": "R$_2$",
    "S": "S",
    "S0": "S$_0$",
    "S2": "S$_2$",
    "SIGMA": R"$\Sigma$",
    "SIGMA0": R"$\Sigma_0$",
    "SIGMA1": R"$\Sigma_1$",
    "T": "T",
    "T2": "T$_2$",
    "U": "U",
    "U0": "U$_0$",
    "U2": "U$_2$",
    "V": "V",
    "V2": "V$_2$",
    "W": "W",
    "W2": "W$_2$",
    "X": "X",
    "X1": "X$_1$",
    "Y": "Y",
    "Y0": "Y$_0$",
    "Y1": "Y$_1$",
    "Y2": "Y$_2$",
    "Z": "Z",
    "Z0": "Z$_0$",
    "Z1": "Z$_1$",
}

# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
