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

import sys

old_dir = set(dir())
old_dir.add("old_dir")

_SUPPORT_FOOTER = "\nPlease contact developers of wulfric (see https://docs.wulfric.org/en/latest/support.html)."


def _raise_with_message(e, message):
    # Python < 3.11
    if sys.version_info[1] < 11:
        args = e.args
        if not args:
            arg0 = message
        else:
            arg0 = f"{args[0]}\n{message}"
        e.args = (arg0,) + args[1:]
        raise e
    # Python >= 3.11
    else:
        e.add_note(message)
        raise e


class ConventionNotSupported(Exception):
    """
    Raised when the convention for the cell/crystall is not one of the supported ones.
    """

    def __init__(self, convention: str, supported_conventions: list):
        self.message = (
            f'Convention "{convention}" is not supported. Supported conventions are\n  * '
            + "\n  * ".join(supported_conventions)
        )

    def __str__(self):
        return self.message


class FailedToDeduceAtomSpecies(Exception):
    r"""
    Raised when the automatic deduction of the atom species from its name fails.
    """

    def __init__(self, name: str):
        self.message = f"Tried to deduce name from '{name}'. Failed."

    def __str__(self):
        return self.message


class NiggliReductionFailed(Exception):
    r"""
    Raised when niggli reduction reaches ``max_iterations``.
    """

    def __init__(self, max_iterations: int):
        self.message = f"Niggli reduction algorithm reached maximum amount of iterations: {max_iterations}"

    def __str__(self):
        return self.message


class PotentialBugError(Exception):
    def __init__(self, error_summary):
        self.message = (
            error_summary
            + "\nIf you see this error, than there might be a bug in wulfric."
            + _SUPPORT_FOOTER
        )

    def __str__(self):
        return self.message


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
