.. _contribute_branches:

************
Branch rules
************

Branches of the upstream repository
===================================

In the upstream repository the releases are made from the ``main`` branch. The
``main`` branch is the default branch in the upstream repository.

For each release we create a tag named ``vMajor.Minor.Patch`` in the upstream repository.

Once new ``Minor`` release is made, the ``Major.Minor`` branch is created for the latest
``Patch`` release of the previous ``Minor`` version. For example, when the ``v0.3.0`` is
released, the ``0.2`` branch is created from the ``v0.2.1`` tag. (Provided that the
latest previous release was ``v0.2.1``.)

The ``Major.Minor`` branches are used for bug fixes in the older versions.

Branches of your local repository
=================================

When you clone the upstream repository, you will have the ``main`` branch checked out by
default.

When you want to contribute to the project, you should create a new branch from ``main``
and name it according to the feature you are working on. If you are fixing a bug, it is
wise to name the branch ``bugfix-issue_number`` when possible.

Branches of origin repository
=============================

At any moment of your work on the feature or bugfix, you can push changes to your forked
repository. For the first push, you should create a new branch in your forked repository.
For example, if you named your local branch as ``new-cool-feature``, type::

    git push -u origin new-cool-feature

It will create a new branch in your forked repository and link your local branch to it.
For the next pushes, you can simply type ``git push``.
