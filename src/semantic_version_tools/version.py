import re
from copy import copy
from functools import total_ordering
from importlib.metadata import version

###################################
# Versioning Class
###################################
#
# This class is used to manage the versioning of the
# software or other products
#
# The versioning is based on the Semantic Versioning 2.0.0
#


__version__ = version("semantic_version_tools")

code = {"d": "devel", "a": "alpha", "b": "beta", "rc": "ReleaseCandidate", "f": "Final"}

numeric_map = {"d": 1, "a": 2, "b": 3, "rc": 4, "f": 5}


@total_ordering
class Vers:
    """
    Class for the manipulation of objects version following the Semantic Versioning

    major.minor.patch-<prerel>.<build>

    Is implemented a special dialect.



    The admitted pre-release values are

        * d  for the developing version
        * a  for the alpha version
        * b  for the beta version
        * rc for the release candidate
        * f  for the final version
    """

    def __init__(self, ver: tuple | str) -> None:

        self.metadata = None
        if isinstance(ver, str):
            match = re.fullmatch(
                r"(\d+)\.(\d+)(?:\.(\d+))?"
                r"(?:[-.]([a-zA-Z]+)(?:\.?(\d+))?)?"
                r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?",
                ver,
            )
            if match is None:
                raise ValueError(f"Invalid version: {ver!r}")

            major, minor, patch, release, build, self.metadata = match.groups()
            ver = (int(major), int(minor))
            if patch is not None or release is not None:
                ver += (int(patch or 0),)
            if release is not None:
                aliases = {
                    "dev": "d",
                    "development": "d",
                    **{name.lower(): key for key, name in code.items()},
                }
                release = release.lower()
                ver += (aliases.get(release, release), int(build or 1))

        if not isinstance(ver, tuple):
            raise TypeError("Version must be a string or tuple")
        if not 2 <= len(ver) <= 5:
            raise ValueError("Version tuple must contain two to five elements")

        self.major, self.minor = ver[:2]
        self._len = min(len(ver), 3)
        self.patch = ver[2] if len(ver) >= 3 else 0
        self.type = ver[3] if len(ver) >= 4 else "f"
        self.build = ver[4] if len(ver) == 5 else 1
        if self.type is not None:
            if not isinstance(self.type, str):
                raise TypeError(
                    "The fourth element of the version number must be a string"
                )
            if self.type not in code:
                raise ValueError(
                    f"The fourth element of the version must be one of {','.join(code)}"
                )

    def full(self) -> str:
        """
        Return the full version

        Returns:
            str: the version string
        """
        if self.type is None or self.type.lower() == "f":
            nVer = self.short()
        # elif:
        #     nVer = f"{self.major}.{self.minor}.{self.patch}"
        else:
            nVer = (
                f"{self.major}.{self.minor}.{self.patch}-{code[self.type]}.{self.build}"
            )
        if self.metadata is not None:
            return f"{nVer}+{self.metadata}"
        return nVer

    def short(self) -> str:
        """
        Return the version in the form major.minor.patch

        Returns:
            str: the version string
        """
        return f"{self.major}.{self.minor}{f'.{self.patch}' if self._len == 3 else ''}"

    def __repr__(self) -> str:
        return f"Version {self.full()}"

    def __str__(self) -> str:
        return f"Version {self.full()}"

    def _precedence(self) -> tuple:
        return (
            self.major,
            self.minor,
            self.patch,
            numeric_map[self.type or "f"],
            self.build,
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vers):
            return NotImplemented
        return self._precedence() == other._precedence()

    def __lt__(self, other) -> bool:
        if not isinstance(other, Vers):
            return NotImplemented
        return self._precedence() < other._precedence()

    def __add__(self, other: "Vers | int | float") -> "Vers":
        result = copy(self)
        if isinstance(other, int):
            result.minor += other
        elif isinstance(other, float):
            major, minor = str(other).split(".")
            result.major += int(major)
            result.minor += int(minor)
        elif isinstance(other, Vers):
            result.major += other.major
            result.minor += other.minor
            if result._len == 3:
                result.patch += other.patch
        else:
            return NotImplemented
        return result
