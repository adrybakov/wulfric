.. _contribute_docs:

*************
Documentation
*************

The documentation of wulfric is build by |sphinx|_.

.. hint::

  The best way to get a feeling about how the documentation of wulfric is structured and
  written is to read its source code in the "docs/source" directory and compare it's
  content and structure with this webpage. If you have any questions we encourage you to
  :ref:`contact us <support>`.

Documentation structure
=======================

Majority of the documentation belongs

* API ("api" folder)

  Semi-automatically generated documentation of the source code, it is mostly build
  from the docstrings of the source code, using |sphinx-autodoc|_ and
  |sphinx-autosummary|_.

  It is located in the "docs/source/api" directory. Its content loosely follows
  the public structure of the package. Functions are recalled by hand, rather that
  automatically to improve readability. Please read existing files to get a feeling about
  the structure of API.

* User guide ("user-guide" folder)
  Hand-written |ReStructuredText-Sphinx|_ files with usage examples and explanation of
  the wulfric's functionality. It is located in the "docs/source/user-guide" directory.

  We separate the user guide into several parts:

  - "usage" folder
    The usage guide is a detailed explanation of the functionality of wulfric, grouped by
    the concepts. The majority of examples (and doctests) are written there.

  - "library" folder
    Description of theory and algorithms behind wulfric. Individual documents/folders
    are located there, however in the toctrees they are placed directly under the
    "user-guide" for better visibility (as opposed to be served from within "library"
    page).

The rest of the documentation is located in the "docs/source" directory and it includes,
among other things:

* "conf.py" file
  The configuration file for the |sphinx|_.

* "index.rst" file

  The main page of the documentation. It includes the table of contents and the
  introduction to the wulfric.

* "support.rst" file

  The page with the information about how to get support for the users of wulfric.

* "release-notes" folder

  The release notes for each version of wulfric.

* "contribute" folder

  Folder for the  documentation of how to contribute to wulfric.

* "img" folder

  All images should be placed here.


Docstrings
==========

All public classes and functions have to have a docstring.
The docstring has to be written in the |numpydoc|_ style guide.

To get a feeling about the style you can read examples in the source code of wulfric.
