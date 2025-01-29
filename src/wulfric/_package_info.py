# Wulfric - Crystal, Lattice, Atoms, K-path.
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

from calendar import month_name
from datetime import datetime

from wulfric import __doclink__, __release_date__, __version__

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def logo(info=None, line_length=None, flat=False, date_time=False, comment=None):
    """
    Logo generator for wulfric package.

    Returns the logo and information about the package.

    Parameters
    ----------
    info : list of str, optional
        Information about the package, that is displayed below the logo.
        Each element should not exceed 50 characters.
        by default it displays the version, release date,
        git hash and documentation link. You can pass th empty list
        to display only the logo.
    line_length : int, optional
        Length of the lines to be returned.
        Minimum value is 62.
    flat : bool
        Whether to return a flat logo or not.
    date_time : bool, default False
        Whether to include the date and time to the standard info or not.
    comment : str or bool, optional
        Whether to use some character at the end of each string. If bool and
        True, then "# " is used. If str, then this string is used. If None, then
        no character is used.
    Returns
    -------
    logo_info : str
        Logo and information about the package.
    """
    if info is None:
        info = [
            f"Version: {__version__}",
            f"Documentation: {__doclink__}",
            f"Release date: {__release_date__}",
            f"Licence: GNU GPLv3",
            f"Copyright (C) 2023-{datetime.now().year}  Andrey Rybakov",
        ]
        if date_time:
            cd = datetime.now()
            info.append("")
            info.append(
                f"Generated on {cd.day} {month_name[cd.month]} {cd.year}"
                + f" at {cd.hour}:{cd.minute}:{cd.second} "
            )
    logo = [
        "██╗      ██╗ ██╗   ██╗ ██╗      ███████╗ ██████╗  ██╗  ██████╗",
        "██║      ██║ ██║   ██║ ██║      ██╔════╝ ██╔══██╗ ██║ ██╔════╝",
        "██║  █╗  ██║ ██║   ██║ ██║      █████╗   ██████╔╝ ██║ ██║     ",
        "██║ ███╗ ██║ ██║   ██║ ██║      ██╔══╝   ██╔══██╗ ██║ ██║     ",
        "╚███╔══███╔╝ ╚██████╔╝ ███████╗ ██║      ██║  ██║ ██║ ╚██████╗",
        " ╚══╝  ╚══╝   ╚═════╝  ╚══════╝ ╚═╝      ╚═╝  ╚═╝ ╚═╝  ╚═════╝",
    ]
    if flat:
        logo = [
            "██       ██  ██    ██  ██       ███████  ██████   ██   ██████",
            "██       ██  ██    ██  ██       ██       ██   ██  ██  ██     ",
            "██   █   ██  ██    ██  ██       █████    ██████   ██  ██     ",
            "██  ███  ██  ██    ██  ██       ██       ██   ██  ██  ██     ",
            " ███   ███    ██████   ███████  ██       ██   ██  ██   ██████",
        ]
    cat = [
        "▄   ▄     ",
        "█▀█▀█     ",
        "█▄█▄█     ",
        " ███   ▄▄ ",
        " ████ █  █",
        " ████    █",
        " ▀▀▀▀▀▀▀▀ ",
    ]

    N = len(logo[0])
    n = len(cat[0]) + 2
    if line_length is None:
        line_length = N
    if line_length < N:
        line_length = N
    if isinstance(comment, bool) and comment:
        comment = "# "
    elif comment is not None:
        comment = str(comment)
    else:
        comment = ""

    logo_info = [f"{x:^{N}}" for x in logo]
    if len(info) > 0:
        if len(info) <= len(cat):
            before = (len(cat) - len(info)) // 2 + (len(cat) - len(info)) % 2
            after = len(cat) - len(info) - before
            for i in range(len(cat)):
                if i < before or i >= len(cat) - after:
                    logo_info.append(f"{' ':{N-n}}{cat[i]:^{n}}")
                else:
                    logo_info.append(f"{info[i-before]:^{N-n}}{cat[i]:^{n}}")
        else:
            before = (len(info) - len(cat)) // 2
            after = len(info) - len(cat) - before
            for i in range(len(info)):
                if i < before or i >= len(info) - after:
                    logo_info.append(f"{info[i-before]:^{N-n}}")
                else:
                    logo_info.append(f"{info[i-before]:^{N-n}}{cat[i-before]:^{n}}")

    logo_info = [f"{comment}{x:^{line_length}}\n" for x in logo_info]
    return "".join(logo_info)[:-1]


def copyright():
    r"""
    Output short license summary for terminal interactions
    """

    return f"""Wulfric Copyright (C) 2023-{datetime.now().year}  Andrey Rybakov
This program comes with ABSOLUTELY NO WARRANTY; for details type 'wulfric warranty'.
This is free software, and you are welcome to redistribute it
under certain conditions; type 'wulfric conditions' for details."""


def warranty():
    r"""
    Output short warranty summary for terminal interactions
    """

    return f"""THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION."""


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
