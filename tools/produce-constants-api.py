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

import wulfric

ROOT_DIR = "."


SC_REFERENCE = r"""

References
==========
.. [1] Setyawan, W. and Curtarolo, S., 2010.
       High-throughput electronic band structure calculations: Challenges and tools.
       Computational materials science, 49(2), pp. 299-312."""

HPKOT_REFERENCE = r"""

References
==========
.. [1] Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
       Band structure diagram paths based on crystallography.
       Computational Materials Science, 128, pp.140-184."""

SECTIONS = {
    "Atoms": ["ATOM_SPECIES", "ATOMIC_MASS", "ATOM_COLORS"],
    "Setyawan and Curtarolo convention": [
        "SC_BRAVAIS_LATTICE_SHORT_NAMES",
        "SC_BRAVAIS_LATTICE_LONG_NAMES",
        "SC_CONVENTIONAL_TO_PRIMITIVE",
        "SC_BRAVAIS_LATTICE_VARIATIONS",
        "SC_DEFAULT_K_PATHS",
    ],
    "Hinuma, Pizzi, Kumagai, Oba, Tanaka convention": [
        "HPKOT_CONVENTIONAL_TO_PRIMITIVE",
        "HPKOT_DEFAULT_K_PATHS",
    ],
    "Kpoints": ["HS_PLOT_NAMES"],
    "Angle conversion": ["TODEGREES", "TORADIANS"],
    "Space Groups": ["INVERSION_SYMMETRY", "CRYSTAL_FAMILY", "CENTRING_TYPE"],
}

DESCRIPTIONS = {
    "ATOM_SPECIES": ("All possible atom species.", "", ""),
    "ATOMIC_MASS": ("Atomic mass", "", ""),
    "ATOM_COLORS": ("Atom colors that are used by default", "", ""),
    "SC_BRAVAIS_LATTICE_SHORT_NAMES": (
        "Short names of the Bravais lattices.",
        "Data are from [1]_",
        SC_REFERENCE,
    ),
    "SC_BRAVAIS_LATTICE_LONG_NAMES": (
        "Long names of the Bravais lattices.",
        "Data are from [1]_",
        SC_REFERENCE,
    ),
    "SC_CONVENTIONAL_TO_PRIMITIVE": (
        "Transformation matrices from conventional cell to primitive cell.",
        "Data are from the Table 2 of [1]_.",
        HPKOT_REFERENCE,
    ),
    "SC_BRAVAIS_LATTICE_VARIATIONS": (
        "List of all possible variations of the Bravais lattices.",
        "Data are from [1]_",
        SC_REFERENCE,
    ),
    "SC_DEFAULT_K_PATHS": (
        "Default k-path for each variation of Bravais lattices.",
        "Data are from [1]_",
        SC_REFERENCE,
    ),
    "HPKOT_DEFAULT_K_PATHS": (
        "Default k-path for each extended Bravais lattice symbols.",
        "Data are from [1]_",
        HPKOT_REFERENCE,
    ),
    "HPKOT_CONVENTIONAL_TO_PRIMITIVE": (
        "Transformation matrices from conventional cell to primitive cell.",
        "Data are from the Table 3 of [1]_.",
        HPKOT_REFERENCE,
    ),
    "TODEGREES": ("Constant that converts radians to degrees.", "", ""),
    "TORADIANS": ("Constant that converts degrees to radians.", "", ""),
    "INVERSION_SYMMETRY": (
        "Whether the space group has inversion as a symmetry operation or not.",
        "",
        "",
    ),
    "CRYSTAL_FAMILY": (
        "Crystal family of every space group.",
        "\nSource can be found `here <https://onlinelibrary.wiley.com/iucr/itc/Ac/ch2o3v0001/>`_.",
        "",
    ),
    "CENTRING_TYPE": (
        "Centring type of every space group.",
        "\nSource can be found `here <https://onlinelibrary.wiley.com/iucr/itc/Ac/ch2o3v0001/>`_.",
        "",
    ),
    "HS_PLOT_NAMES": ("Names of high symmetry k points written in LaTex.", "", ""),
}


def float_processor(name, value):
    return f".. code-block:: python\n\n    {name} = {value}"


def tuple_processor(name, value):
    return (
        f".. code-block:: python\n\n    {name} = (\n        "
        + ",\n        ".join(value)
        + ",\n    )"
    )


def dict_processor_str(name, value):
    return (
        f".. code-block:: python\n\n    {name} = "
        + "{\n        "
        + ",\n        ".join([f'"{key}" : "{value[key]}"' for key in value])
        + ",\n    }"
    )


def dict_processor_bool(name, value):
    return (
        f".. code-block:: python\n\n    {name} = "
        + "{\n        "
        + ",\n        ".join([f'"{key}" : {value[key]}' for key in value])
        + ",\n    }"
    )


def dict_processor_3x3_array(name, value):
    def get_str_repr(array):
        return "\n".join(
            [
                "np.array(",
                "            [",
                f"                [{array[0, 0]:.1f}, {array[0, 1]:.1f}, {array[0, 2]:.1f}],",
                f"                [{array[1, 0]:.1f}, {array[1, 1]:.1f}, {array[1, 2]:.1f}],",
                f"                [{array[2, 0]:.1f}, {array[2, 1]:.1f}, {array[2, 2]:.1f}],",
                "            ]",
                "        )",
            ]
        )

    return (
        f".. code-block:: python\n\n    {name} = "
        + "{\n        "
        + ",\n        ".join([f'"{key}" : {get_str_repr(value[key])}' for key in value])
        + ",\n    }"
    )


VALUE_PROCESSORS = {
    "ATOM_SPECIES": tuple_processor,
    "ATOMIC_MASS": dict_processor_str,
    "ATOM_COLORS": dict_processor_str,
    "SC_BRAVAIS_LATTICE_SHORT_NAMES": dict_processor_str,
    "SC_BRAVAIS_LATTICE_LONG_NAMES": dict_processor_str,
    "SC_CONVENTIONAL_TO_PRIMITIVE": dict_processor_3x3_array,
    "SC_BRAVAIS_LATTICE_VARIATIONS": tuple_processor,
    "SC_DEFAULT_K_PATHS": dict_processor_str,
    "HPKOT_DEFAULT_K_PATHS": dict_processor_str,
    "HPKOT_CONVENTIONAL_TO_PRIMITIVE": dict_processor_3x3_array,
    "TODEGREES": float_processor,
    "TORADIANS": float_processor,
    "INVERSION_SYMMETRY": dict_processor_bool,
    "CRYSTAL_FAMILY": dict_processor_str,
    "CENTRING_TYPE": dict_processor_str,
    "HS_PLOT_NAMES": dict_processor_str,
}


def main():
    lines = (
        [
            ".. _api_constants:",
            "",
            "*****************",
            "wulfric.constants",
            "*****************",
            "",
            ".. toctree::",
            "    :hidden:",
            "",
        ]
        + [f"    {key.lower()}" for key in DESCRIPTIONS]
        + ["\n"]
    )

    for section in SECTIONS:
        table_length_1 = max([len(element) for element in SECTIONS[section]]) + 21
        table_length_2 = max(
            [len(DESCRIPTIONS[element][0]) for element in SECTIONS[section]]
        )

        lines = (
            lines
            + [
                section,
                "=" * len(section),
                "",
                "=" * table_length_1 + " " + "=" * table_length_2,
            ]
            + [
                f"{f':ref:`api_constants_{element}`':<{table_length_1}} {DESCRIPTIONS[element][0]}"
                for element in SECTIONS[section]
            ]
            + ["=" * table_length_1 + " " + "=" * table_length_2, ""]
        )

    with open(
        os.path.join(ROOT_DIR, "docs", "source", "api", "constants", "index.rst"), "w"
    ) as f:
        f.write("\n".join(lines))

    for key in DESCRIPTIONS:
        lines = [
            f".. _api_constants_{key}:",
            "",
            "*" * len(f"wulfric.constants.{key}"),
            f"wulfric.constants.{key}",
            "*" * len(f"wulfric.constants.{key}"),
            "",
            DESCRIPTIONS[key][0],
            "",
            DESCRIPTIONS[key][1],
            "",
            VALUE_PROCESSORS[key](
                name=key, value=wulfric.constants.__getattribute__(key)
            ),
        ]

        if len(DESCRIPTIONS[key][2]) > 0:
            lines.append(DESCRIPTIONS[key][2])

        with open(
            os.path.join(
                ROOT_DIR, "docs", "source", "api", "constants", f"{key.lower()}.rst"
            ),
            "w",
        ) as f:
            f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
