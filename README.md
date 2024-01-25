# pyOMA2

[![python](https://img.shields.io/badge/Python-3.8-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

_______________________

This is the new and updated version of pyOMA module, a Python module designed for conducting operational modal analysis. With this update, we've transformed pyOMA from a basic collection of functions into a more sophisticated module that fully leverages the capabilities of Python classes. The module now supports analysis of both single and multi-setup data measurements, which includes handling multiple acquisitions with a mix of reference and roving sensors. We've also introduced interactive plots, allowing users to select desired modes for extraction directly from the plots generated by the algorithms. Additionally, a new feature enables users to define the geometry of the structures being tested, facilitating the visualization of mode shapes after modal results are obtained. The underlying functions of these classes have been rigorously revised, resulting in significant enhancements and optimizations.

Please note that this is still an alpha release, and we are continuously refining the docstrings, documentation, and other aspects of the module. However, we have provided three working examples that demonstrate the module's capabilities: Example_SS.py (for single setup), Example_MSpoSER.py (for multi setups using the Post-Single Estimation Rescaling method), and Example_MSpreGER.py (for multi setups using the Pre-Global Estimation Rescaling method).

## Quick start

To see example usage go to `pyoma2/Example*` files.

To run them, after have installed the package you can do as follow:

**Unix**

```shell
pyoma2_example_SS
pyoma2_example_MSposER
pyoma2_example_MSpreGER
```

**Windows**

```python
from pyoma2.Example_MSpoSER import main as main_MSpoSER
from pyoma2.Example_MSpreGER import main as main_MSpreGER
from pyoma2.Example_SS import main as main_SS


if __name__ == '__main__':
    main_MSpoSER()
```
