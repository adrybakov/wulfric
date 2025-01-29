.. _contribute_docs:

*************
Documentation
*************

The documentation of wulfric is build by |sphinx|_.

.. hint::

  The best way to get a feeling about how the documentation of wulfric is structured is to read
  the source code in the "docs/source" directory and compare it's content and structure with this webpage.
  If you have any questions we encourage you to :ref:`contact us <support>`.

Documentation structure
=======================

The documentation falls into two big parts:

* API ("api" folder)

  Semi-automatically generated documentation of the source code, it is mostly build
  based on the docstrings of the source code, using |sphinx-autodoc|_ and |sphinx-autosummary|_.

  It is located in the "docs/source/api" directory. Its content loosely follows
  the structure of the source code folders. The methods and classes are listed manually
  for the better presentation of the documentation, the rest is automatically generated.
  Please read existing files to get a feeling about the structure.

* User guide ("user-guide" folder)
  Hand-written ReStructuredText files with the usage examples and the explanation of the
  functionality of the wulfric. It is located in the "docs/source/user-guide" directory.

  We separate the user guide into several parts:

  - "module" folder
    The module guide is a detailed explanation of the functionality of the classes and
    functions, grouped by logical modules. The majority of examples (and doctests) are
    written here.

  - "library" folder
    Description of theory and algorithms behind the wulfric.  Individual documents/folders
    are located there, however in the toctrees they are placed directly under the "user-guide"
    for better visibility (as opposed to be served from within "library" folder).


  At the moment we have a few rules formulated for the documentation of the python module:

  - Each function and class has to have "Import" section.
  - Each class has to have "Creation" section.
  - Each page of the module guide have to have the link to the corresponding page of the API.

The rest of the documentation is located in the "docs/source" directory and it includes,
among other things:

* "conf.py" file
  The configuration file for the |sphinx|_.

* "index.rst" file

  The main page of the documentation. It includes the table of contents and the introduction
  to the wulfric.

* "support.rst" file

  The page with the information about how to get support for the users of wulfric.

* "release-notes" folder

  The release notes for each version of wulfric.

* "contribute" folder

  Root folder for the  documentation of how to contribute to wulfric.


Docstrings
==========

All public classes and functions have to have a docstring.
The docstring has to be written in the |numpydoc|_ style guide.

To get a feeling about the style you can read examples in the source code of wulfric.
