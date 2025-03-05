
# Version-Tools

## Installation

### From Repository

To install the Version-Tools package from the repository, run the following commands:

```sh
git clone https://github.com/RomoloPoliti-INAF/version-tools.git
cd version-tools
poetry install
```

### From PyPi

To install the Version-Tools package from PyPi, run the following command:

```sh
pip install semantic-version-tools
```
### Using poetry

To add the package to your poetry project, you can run the command:

```sh
poetry add semantic-versioning-tools
```


## Usage

To use the library it's necessary import the class *Vers*, than you can comapare or manipulate the version numbers.

### Initialize and print version

```python
>>> from semantic_version_tools import Vers

>>> main_ver=Vers('1.0')
>>> print(main_ver)

Version 1.0
```

The version number could be a string or a tuple, whit 2 or 5 elements:
- the major version number
- the minor version number
- the patch number
- pre-release type
- build number

For the pre-release are used letters as reported below:

- **d**: developing version
- **a**: alpha release
- **b**: beta release
- **rc**: release candidate
- **f**: final release

```python
>>> main_version = Vers((0,1,0,'d',1))
>>> print(main_version)

Version 0.1.0-devel.1

>>> main_version = Vers('0.1.0-a.1')
>>> print(main_version)

Version 0.1.0-alpha.1
```

### Compare versions

In the class Vers are implemented the main comparison operators.
For example:

```python
>>> a=Vers('1.0.0')
>>> b=Vers('1.0.1')

>>> a>b
False
>>> a==b
False
>>> a<b
True
a<=b
True
```

### Sum and increase

It's possible sum tro version number or icrease it.

```python
>>> a = Vers('1.0.0')
>>> b = Vers('1.0.1')
>>> c=a+b
>>> c
Version 2.0.1


>>> a = Vers('1.0.0')
>>> a=a+1
>>> a
Version 1.1.0
# equivalent to
>>> a +=1
>>> a
Version 1.1.0
```

The summ add a minor version. To add a major version you must add a float

```python
>>> a = Vers('1.0.0')
>>> a += 1.0
>>> a
Version 2.0.0
```