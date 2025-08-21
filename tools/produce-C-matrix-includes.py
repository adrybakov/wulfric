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
import os

import numpy as np

from wulfric.constants import CONVENTIONAL_TO_PRIMITIVE as C_MATRICES

ROOT_DIR = "."
OUTPUT_PATH = os.path.join(
    ROOT_DIR, "docs", "source", "user-guide", "conventions", "bravais-lattices"
)


def main():
    for lattice_type in C_MATRICES:
        folder_name = lattice_type.lower()

        C = C_MATRICES[lattice_type]
        Ci = np.linalg.inv(C)

        text = (
            R".. math::",
            "",
            R"    \boldsymbol{C}",
            "    =",
            R"    \begin{pmatrix}",
            f"        {C[0][0]:g} & {C[0][1]:g} & {C[0][2]:g} " R"\\",
            f"        {C[1][0]:g} & {C[1][1]:g} & {C[1][2]:g} " R"\\",
            f"        {C[2][0]:g} & {C[2][1]:g} & {C[2][2]:g} " R"\\",
            R"    \end{pmatrix}",
            R"    \qquad",
            R"    \boldsymbol{C}^{-1}",
            "    =",
            R"    \begin{pmatrix}",
            f"        {Ci[0][0]:g} & {Ci[0][1]:g} & {Ci[0][2]:g} " R"\\",
            f"        {Ci[1][0]:g} & {Ci[1][1]:g} & {Ci[1][2]:g} " R"\\",
            f"        {Ci[2][0]:g} & {Ci[2][1]:g} & {Ci[2][2]:g} " R"\\",
            R"    \end{pmatrix}",
            "",
        )

        with open(os.path.join(OUTPUT_PATH, folder_name, "C_matrix.inc"), "w") as file:
            file.write("\n".join(text))


# .. math::

#     \boldsymbol{C}
#     =
#     \begin{pmatrix}
#       -1 & 1 & 1 \\
#       1 & -1 & 1 \\
#       1 & 1 & -1
#     \end{pmatrix}
#     \qquad
#     \boldsymbol{C}^{-1}
#     =
#     \dfrac{1}{2}
#     \begin{pmatrix}
#       0 & 1 & 1 \\
#       1 & 0 & 1 \\
#       1 & 1 & 0
#     \end{pmatrix}


if __name__ == "__main__":
    main()
