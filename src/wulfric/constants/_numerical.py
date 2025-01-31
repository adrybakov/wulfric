# Wulfric - Cell, Atoms, K-path.
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


from math import pi

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")

# For the linear spatial variables. If two points are closer than EPS_LENGTH,
# then they are considered to be the same.
EPS_LENGTH = 1e-8

# For the angular variables, in degrees. If two angles differs less than EPS_ANGLE,
# then they are considered to be the same.
EPS_ANGLE = 1e-4

# MIN_LENGTH is a direct consequence of the EPS_LENGTH:
MIN_LENGTH = EPS_LENGTH
# MAX_LENGTH is a direct consequence of the EPS_LENGTH:
# Inverse of the MAX_LENGTH in the real space has to be meaningful
# in the reciprocal space (>= EPS_LENGTH).
MAX_LENGTH = 1 / EPS_LENGTH

# MIN_ANGLE is a direct consequence of the EPS_ANGLE
MIN_ANGLE = EPS_ANGLE  # In degrees
# No need to define MAX_ANGLE, as it is restricted by 2 pi in the context of wulfric.

# Relative and Absolute accuracy for comparison of two float numbers in the sense
# of numpy.allclose(). Used almost exclusively for unit tests.
ATOL = 1e-8
RTOL = 1e-5


################################################################################
#                                   Numerical                                  #
################################################################################
TODEGREES = 180.0 / pi


TORADIANS = pi / 180.0

# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
