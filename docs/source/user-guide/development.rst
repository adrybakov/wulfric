.. _user-guide_start_development:

*************************
Development and stability
*************************

Versions of wulfric are labeled in a standard way as ``major.minor.patch``. For example,
version ``0.4.0`` is decoded as ``0`` major version, ``4`` minor version and ``0`` patch
version.

The development of wulfric proceeds in two stages, that are reflected in the versions of
the package. The principles listed here were formulated with the release ``0.5.0``.

Beta stage (0.*.*)
==================

Unstable stage of development. Change of the ``minor`` version does not guarantee backward
compatibility and may introduce changes of interface, may introduce changes of the public
data-structure.

This stage allows the code to mature and reflect the best approaches for the problems that
it is aimed for.

No timeline is set for the Beta stage.

It is recommended to fix the minor version at this stage (i.e. use ``wulfric==0.5.*`` to
fix 5th minor version).

Stable stage (>=1.*.*)
======================

When the code is mature enough, the first stable version will be published. Starting from
the major version greater than ``1`` the code is considered to be stable. Minor versions
might introduce new functionalities, but they would not break the old ones, neither
compromise backward-compatibility.

Obsolete functions either kept or supported for at least two consecutive minor version
changes (but no less than for two years) with ``DeprecationWarning`` before removal.

Change of the ``major`` version is not expected. However, new ``major`` release is
not forbidden if the changes are breaking the principles of a ``minor`` release
and are inevitable.
