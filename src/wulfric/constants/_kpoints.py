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
    "A": R"A",
    "A0": R"A$_0$",
    "A1": R"A$_1$",
    "B": R"B",
    "B0": R"B$_0$",
    "B1": R"B$_1$",
    "B2": R"B$_2$",
    "C": R"C",
    "C0": R"C$_0$",
    "C1": R"C$_1$",
    "C2": R"C$_2$",
    "C4": R"C$_4$",
    "D": R"D",
    "D0": R"D$_0$",
    "D1": R"D$_1$",
    "D2": R"D$_2$",
    "DELTA0": R"$\Delta_0$",
    "E": R"E",
    "E0": R"E$_0$",
    "E2": R"E$_2$",
    "E4": R"E$_4$",
    "F": R"F",
    "F0": R"F$_0$",
    "F1": R"F$_1$",
    "F2": R"F$_2$",
    "F3": R"F$_4$",
    "F4": R"F$_4$",
    "G": R"G",
    "G0": R"G$_0$",
    "G2": R"G$_2$",
    "G4": R"G$_4$",
    "G6": R"G$_6$",
    "GAMMA": R"$\Gamma$",
    "H": R"H",
    "H0": R"H$_0$",
    "H1": R"H$_1$",
    "H2": R"H$_2$",
    "H4": R"H$_4$",
    "H6": R"H$_6$",
    "I": R"I",
    "I1": R"I$_1$",
    "I2": R"I$_2$",
    "J0": R"J$_0$",
    "K": R"K",
    "K2": R"K$_2$",
    "K4": R"K$_4$",
    "L": R"L",
    "L0": R"L$_0$",
    "L1": R"L$_1$",
    "L2": R"L$_2$",
    "L4": R"L$_4$",
    "LAMBDA0": R"$\Lambda_0$",
    "M": R"M",
    "M0": R"M$_0$",
    "M1": R"M$_1$",
    "M2": R"M$_2$",
    "M4": R"M$_4$",
    "M6": R"M$_6$",
    "M8": R"M$_8$",
    "N": R"N",
    "N1": R"N$_1$",
    "N2": R"N$_2$",
    "N4": R"N$_4$",
    "N6": R"N$_6$",
    "P": R"P",
    "P0": R"P$_0$",
    "P1": R"P$_1$",
    "P2": R"P$_2$",
    "Q": R"Q",
    "Q0": R"Q$_0$",
    "Q1": R"Q$_1$",
    "R": R"R",
    "R0": R"R$_0$",
    "R2": R"R$_2$",
    "S": R"S",
    "S0": R"S$_0$",
    "S2": R"S$_2$",
    "S4": R"S$_4$",
    "S6": R"S$_6$",
    "SIGMA": R"$\Sigma$",
    "SIGMA0": R"$\Sigma_0$",
    "SIGMA1": R"$\Sigma_1$",
    "T": R"T",
    "T2": R"T$_2$",
    "U": R"U",
    "U0": R"U$_0$",
    "U2": R"U$_2$",
    "V": R"V",
    "V0": R"V$_0$",
    "V2": R"V$_2$",
    "W": R"W",
    "W2": R"W$_2$",
    "X": R"X",
    "X1": R"X$_1$",
    "X2": R"X$_2$",
    "Y": R"Y",
    "Y0": R"Y$_0$",
    "Y1": R"Y$_1$",
    "Y2": R"Y$_2$",
    "Y4": R"Y$_4$",
    "Z": R"Z",
    "Z0": R"Z$_0$",
    "Z1": R"Z$_1$",
    "Z2": R"Z$_2$",
}

# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
