**Deprecated** - Construct 0.2.X will include install scripts in the main construct repo.

construct_setup
===============
Setup construct core packages.

+---------------------+------------------------------+---------+
| package             | description                  | version |
+=====================+==============================+=========+
| construct_          | Core api                     | 0.1.30  |
+---------------------+------------------------------+---------+
| construct_cpenv_    | Cpenv Integration            | 0.2.0   |
+---------------------+------------------------------+---------+
| construct_launcher_ | Application launcher         | 0.1.5   |
+---------------------+------------------------------+---------+
| construct_maya_     | Autodesk Maya integration    | 0.1.13  |
+---------------------+------------------------------+---------+
| construct_nuke_     | The Foundry Nuke integration | 0.1.10  |
+---------------------+------------------------------+---------+
| construct_ui_       | Graphical user interface     | 0.2.3   |
+---------------------+------------------------------+---------+
| fsfs_               | File system metadata         | latest  |
+---------------------+------------------------------+---------+


Installation
============

Construct requires Git_ and Python 2.7 or 3.4+. The best method of installing
construct is to use the install scripts included in this repository. These
install construct into custom locations and allow for installing multiple
versions of construct alongside each other. A symlink is created linking the
current version upon install.

Windows
-------
Launch a command prompt as an Administrator and run the following commands.

.. code-block:: console

    > cd %TMP%
    > git clone https://github.com/construct-org/construct_setup
    > cd construct_setup
    > install

The default install path on windows is :code:`C:\Construct`.

Linux and Mac
-------------
Launch a terminal and run the following commands.

.. code-block:: console

    > git clone https://github.com/construct-org/construct_setup
    > cd construct_setup
    > sudo -s
    > source install.sh

The default install path on Linux and Mac is :code:`/opt/construct`.

Test your install
-----------------
After installing you should have access to the construct cli.

.. code-block:: console

    > cons

Installation Options
--------------------

.. code-block:: console

    optional arguments:
      -h, --help         show this help message and exit
      --version VERSION
      --python PYTHON    Python Executable
      --where WHERE      Where to install
      --config CONFIG    Location of a construct configuration file.
      --local            Install from local directory.

Advanced: Install via pip
-------------------------
You can install construct via pip but you will be forced to manage versioning
yourself.

.. code-block:: console

    pip install PySide2
    pip install -I git+git://github.com/construct-org/construct_setup.git

.. _construct: https://github.com/construct-org/construct
.. _construct_cpenv: https://github.com/construct-org/construct_cpenv
.. _construct_launcher: https://github.com/construct-org/construct_launcher
.. _construct_maya: https://github.com/construct-org/construct_maya
.. _construct_nuke: https://github.com/construct-org/construct_nuke
.. _construct_ui: https://github.com/construct-org/construct_ui
.. _fsfs: https://github.com/danbradham/fsfs
.. _Git: https://git-scm.com
