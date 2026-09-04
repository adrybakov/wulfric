.. _user-guide_start_development:

*************************
Development and stability
*************************

Versions of Wulfric are labeled in a standard way as ``major.minor.patch``. For
example, version ``0.4.0`` denotes major version ``0``, minor version ``4`` and
patch version ``0``.

The development of Wulfric proceeds in two stages that are reflected in the
versions of the package. The principles listed here were formulated at the
release ``0.5.0``.

Beta stage (0.*.*)
==================

Unstable stage of development. Change of the ``minor`` version does not
guarantee backward compatibility and may introduce changes to the interface or
the public data structures.

This stage allows the code to mature and reflect the best approaches to the
problems it aims to solve.

No timeline is set for the Beta stage.

It is recommended to fix the minor version at this stage (i.e. use ``wulfric==0.5.*`` to
fix 5th minor version).

Stable stage (>=1.*.*)
======================

When the code is mature enough, the first stable version will be published.
Starting from the major version ``1`` the code is considered to be stable. Minor
versions introduce new functionalities without breaking existing behavior or
backward compatibility.

Obsolete functions are supported for at least two consecutive minor version
changes (but no less than for two years) and emit a ``DeprecationWarning``.

Change of the ``major`` version is not expected. Overall, we intend to avoid
breaking changes and stay on ``1.x.x``. However, a new ``major`` release is not
forbidden if the changes are breaking the principles of a ``minor`` release and
are inevitable.

You can safely depend on ``>=1.0,<2.0``.
