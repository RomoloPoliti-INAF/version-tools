import pytest
from version_tools.version import Vers


def test_version_initialization():
    v1 = Vers((1, 0, 0))
    assert v1.major == 1
    assert v1.minor == 0
    assert v1.patch == 0
    assert v1.type is None
    assert v1.build is None

    v2 = Vers("1.0.0")
    assert v2.major == 1
    assert v2.minor == 0
    assert v2.patch == 0
    assert v2.type == "f"
    assert v2.build == 1

    v3 = Vers("1.0.0-alpha.1")
    assert v3.major == 1
    assert v3.minor == 0
    assert v3.patch == 0
    assert v3.type == "a"
    assert v3.build == 1

def test_version_full():
    v1 = Vers((1, 0, 0))
    assert v1.full() == "1.0.0"

    v2 = Vers("1.0.0-alpha.1")
    assert v2.full() == "1.0.0-alpha.1"

def test_version_short():
    v1 = Vers((1, 0, 0))
    assert v1.short() == "1.0.0"

    v2 = Vers("1.0.0-alpha.1")
    assert v2.short() == "1.0.0"

def test_version_comparison():
    v1 = Vers((1, 0, 0))
    v2 = Vers((1, 0, 1))
    v3 = Vers("1.0.0-alpha.1")
    v4 = Vers("1.0.0-beta.1")

    assert v1 < v2
    assert v2 > v1
    assert v1 != v2
    assert v1 == Vers((1, 0, 0))
    assert v3 < v4
    assert v4 > v3
    assert v3 != v4

def test_version_exceptions():
    with pytest.raises(Exception):
        Vers((1, 0, 0, 1))

    with pytest.raises(ValueError):
        Vers((1, 0, 0, "invalid"))

if __name__ == "__main__":
    pytest.main()