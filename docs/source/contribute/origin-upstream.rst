.. _contribute_origin-upstream:

*******************
Origin and Upstream
*******************

We use the terminology **Upstream** and **Origin** for the two remote repositories that
are used in the development process. Relationships between them and the local repository
with the most common command for communication between them is

.. figure:: img/origin-upstream-local.png
    :target: ../_images/origin-upstream-local.png
    :align: center

Origin repository
=================

**Origin** is a wulfric repository under **your** personal account.

During the development you push the changes to **Origin**. Once the feature you're working
on is ready, you will create a pull request from **Origin** to **Upstream**.

Upstream repository
===================

**Upstream** is a  main |repo|_, from which the release is made.

You can pull changes from the **Upstream** to your local repository to keep it up to date
and then push the changes to **Origin**. Alternatively, you can  *sync fork* using github
web interface to keep your **Origin** up to date and then pull the change to your local
repository from **Origin**.

Local repository
================

The local repository is the repository on your computer where you will be making changes
to the code and committing them. Typically, you will be pushing your changes to
**Origin** and pulling changes made by others from **Upstream**.
