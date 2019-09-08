Scripts to run as CWL with two workflow managers:
* [Rabix](https://rabix.io/).  Rabix Executor is no longer maintained but still serves as a lightweight local reference
* [Cromwell](https://cromwell.readthedocs.io/en/develop/).  Developed specifically for MGI environment

Note: it is suggested that you do not use `conda` to set environment when running Cromwell at MGI, since it pollutes python
paths and may lead to library not found errors.  Turn off conda with, `conda config --set auto_activate_base false`
