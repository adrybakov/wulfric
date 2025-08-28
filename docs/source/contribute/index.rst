.. _contribute:

*******************
Contributor`s guide
*******************


We welcome the contribution to the package!

If you're interested in seeing who has already contributed to this project, please visit
our :ref:`Contributors page <contribute_contributors>`. We appreciate all contributions
and look forward to see your name on that list!

It is not necessary to be a programmer to contribute. You can help with documentation,
:ref:`new features <contribute_feature>` and :ref:`finding bugs <contribute_bug>`.


Contribution to the source code is summarized below. We assume that you have an account on
`<https://github.com>`_ and familiar with `Git <https://git-scm.com/>`_.

Development workflow
====================

Fork and clone
--------------

* Go to the |repo|_ and click on the "Fork" button.
  Now you have your own copy of the wulfric repository in your GitHub account.
* Clone your copy of the repository to your local machine:

  - If you are using ssh-key::

      git clone git@github.com:your-username/wulfric.git

  - If you are not using ssh-key::

      git clone https://github.com/your-username/wulfric.git

* Change the directory::

    cd wulfric

* Add the :ref:`upstream <contribute_origin-upstream>` repository::

    git remote add upstream https://github.com/adrybakov/wulfric.git

* Pull the latest changes from the wulfric repository if necessary::

    git pull upstream main

Set up the environment
----------------------

We recommend to use virtual environment (with |venv|_, for example). Once the virtual
environment is created, you can install requirements:

* Package dependencies::

    pip install -r requirements.txt

* Development tools::

    pip install -r requirements-dev.txt

* Documentation tools::

    pip install -r docs/requirements.txt

* Testing tools::

    pip install -r tests/requirements.txt

.. note::
  For the linux and OSX systems there is a scenario defined.
  It installs all requirements. Note: it does NOT create an environment for you::

    make requirements

Enable pre-commit
-----------------

We use `pre-commit <https://pre-commit.com/>`_ to enforce some rules on the code style
before each commit.
To enable it, run the following command::

  pre-commit install

Now, every time you commit the code, pre-commit will check it for you.

.. hint::
  If you want to run pre-commit manually, you can use the following command::

    pre-commit run --all-files

Develop your contribution
-------------------------

* Create a :ref:`dedicated branch <contribute_branches>` for your feature,
  that you are going to develop::

    git checkout -b feature-name

* Develop your contribution. Commit your progress locally
  (`git-add <https://git-scm.com/docs/git-add>`_
  and `git-commit <https://git-scm.com/docs/git-commit>`_).
  Use |good-commit-messages|_. Write :ref:`tests <contribute_tests>`.
  Write :ref:`documentation <contribute_docs>`.

Submit your contribution
------------------------

* Push the changes to your forked repository::

    git push origin feature-name

* Go to your forked repository on GitHub and click on the
  green "Compare & pull request" button.
  Describe your contribution and submit the pull request.
  Please mention the issue number if it is related to any.

Review and merge
----------------

* Once the pull request is submitted, the code will be reviewed.
  If there are any comments, please fix them. You can push the changes to the
  same branch and they will be added to the pull request automatically.
* Once the pull request is approved, it will be merged to the
  `main <https://github.com/adrybakov/wulfric>`_ branch.


Development process in details
==============================

.. toctree::
  :hidden:

  contributors

.. toctree::
  :maxdepth: 2

  features
  bugs
  documentation
  tests
  origin-upstream
  branches
