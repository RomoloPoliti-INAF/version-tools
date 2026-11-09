# Version-Tools

`semantic-version-tools` provides `Vers`, a Python class for parsing,
comparing and incrementing version numbers. It supports Python 3.10–3.15.

## Installation

Install from PyPI with pip or add the package to a uv project.

```sh
pip install semantic-version-tools
uv add semantic-version-tools
```

## Usage

```pycon
>>> from semantic_version_tools import Vers
>>> Vers("1.2")
Version 1.2
>>> Vers((1, 2, 0, "d", 1))
Version 1.2.0-devel.1
>>> Vers("1.2-dev.1+sha.abc").full()
'1.2.0-devel.1+sha.abc'
>>> Vers("1.2.0-rc.1") < Vers("1.2.0")
True
```

Tuples contain two to five fields in this order: major, minor, patch,
prerelease code and build number. The prerelease codes are `d` (development),
`a` (alpha), `b` (beta), `rc` (release candidate) and `f` (final).
A prerelease string with an omitted patch uses patch zero. Metadata after
`+` is preserved in the full version and ignored in comparisons.
`short()` returns the numeric version without the prerelease or metadata.

Addition returns a new `Vers` instance. Integers increment the minor
component. Floats use the integer and fractional digits as major and minor
increments. Adding another `Vers` combines the numeric components and
preserves the left operand's precision and release information.

```pycon
>>> current = Vers("1.2.3")
>>> current + 1
Version 1.3.3
>>> current + 1.2
Version 2.4.3
>>> current
Version 1.2.3
>>> current += Vers("1.0.1")
>>> current
Version 2.2.4
```

## Development

```sh
git clone https://github.com/RomoloPoliti-INAF/version-tools.git
cd version-tools
uv sync --locked
uv run --locked ruff check
uv run --locked ruff format --check
uv run --locked pytest --cov=semantic_version_tools --cov-branch --cov-report=term-missing --cov-fail-under=80
uv build
```
