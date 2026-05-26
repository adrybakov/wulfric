# ================================== LICENSE ===================================
# Wulfric - Cell, Atoms, K-path, visualization.
# Copyright (C) 2023 Andrey Rybakov
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
def test(no_logo=False):
    r"""
    Runs unit tests for the whole Wulfric package.

    .. versionadded:: 0.7.0 Test suite is made part of the installable package.

    Parameters
    ----------
    no_logo : bool, default=False
        If ``False``, the Wulfric logo will be printed before running tests.
        Set to ``True`` to suppress the logo.

    Notes
    -----

    Tests depend on two external packages: |pytest|_ and |hypothesis|_. These are not
    dependencies of Wulfric, so you need to install them separately to run tests. You can
    do so with pip (you may need to use ``pip3`` instead of ``pip`` depending on your
    Python setup):

    .. code-block:: bash
        pip install pytest hypothesis

    """

    # Check that pytest is installed
    try:
        import pytest
    except ImportError:
        print(
            "Require package 'pytest' to run tests. Install it with 'pip install pytest'."
        )
        return

    # Check that hypothesis is installed
    # Note: Use importlib.util.find_spec() to avoid rewrite warnings of pytest later on
    import importlib.util

    hypothesis_spec = importlib.util.find_spec("hypothesis")
    if not hypothesis_spec:
        print(
            "Require package 'hypothesis' to run tests. Install it with 'pip install hypothesis'."
        )
        return

    if not no_logo:
        from wulfric._package_info import logo

        print(logo())
        print("Running tests...\n")
    pytest.main(
        [
            "--pyargs",
            "wulfric",
            "-s",
            # Atom deduction in meaningless examples
            "-W ignore:Atom species deduction failed",
            # Deprecation warning for lepage() function
            "-W ignore:wulfric.lepage() is deprecated",
            # Overflow in the edge case of get_angle()
            "-W ignore: overflow encountered in dot",
        ]
    )
