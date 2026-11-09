import pytest

from semantic_version_tools.version import Vers


def test_version_initialization():
    v1 = Vers((1, 0, 0))
    assert v1.major == 1
    assert v1.minor == 0
    assert v1.patch == 0
    assert v1.type == "f"
    assert v1.build == 1

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
    with pytest.raises(TypeError):
        Vers((1, 0, 0, 1))

    with pytest.raises(ValueError):
        Vers((1, 0, 0, "invalid"))


def test_version_sum():
    v1 = Vers((1, 0, 0))
    v2 = Vers((1, 0, 1))
    assert v1 + v2 == Vers((2, 0, 1))


def test_version_sum_integer():
    v1 = Vers((1, 0, 0))
    assert v1 + 1 == Vers((1, 1, 0))


def test_version_sum_float():
    v1 = Vers((1, 0, 0))
    assert v1 + 1.2 == Vers((2, 2, 0))


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("1.2-dev.1", "1.2.0-devel.1"),
        ("1.2.0-devel.1", "1.2.0-devel.1"),
        ("1.2.3-rc.2+sha.abc-123", "1.2.3-ReleaseCandidate.2+sha.abc-123"),
        ("1.2.3+meta", "1.2.3+meta"),
        ("1.2", "1.2"),
    ],
)
def test_full_version_round_trip(source, expected):
    version = Vers(source)
    assert version.full() == expected
    assert Vers(expected) == version
    assert str(version) == repr(version) == f"Version {expected}"


@pytest.mark.parametrize(
    "source", ["abc", "1.2.3!", "1.2.3+", "1.2.3+one..two", "1.2.3-x"]
)
def test_invalid_version_strings(source):
    with pytest.raises(ValueError):
        Vers(source)


def test_metadata_does_not_affect_precedence():
    assert Vers("1.2.3+first") == Vers("1.2.3+second")
    assert Vers("1.2.3-rc.1+first") < Vers("1.2.3+second")


def test_comparison_with_other_types_and_implicit_final():
    version = Vers((1, 2, 3, None))
    assert version == Vers("1.2.3")
    assert version >= Vers("1.2.3")
    assert version <= Vers("1.2.3")
    assert version != "1.2.3"
    with pytest.raises(TypeError):
        assert version < "1.2.3"


@pytest.mark.parametrize(
    ("increment", "expected"),
    [(1, "1.3.3"), (1.2, "2.4.3"), (Vers("1.2.3"), "2.4.6")],
)
def test_addition_preserves_operands(increment, expected):
    version = Vers("1.2.3+meta")
    result = version + increment
    assert result is not version
    assert result.full() == f"{expected}+meta"
    assert version.full() == "1.2.3+meta"
    if isinstance(increment, Vers):
        assert increment.full() == "1.2.3"


def test_augmented_addition_rebinds_and_preserves_short_format():
    version = original = Vers("1.2")
    version += Vers("1.2.3")
    assert version.full() == "2.4"
    assert original.full() == "1.2"


def test_addition_rejects_unsupported_operands():
    with pytest.raises(TypeError):
        Vers("1.2.3") + "1.2.3"


@pytest.mark.parametrize("source", [(), (1,), (1, 2, 3, "a", 1, 2)])
def test_invalid_tuple_length(source):
    with pytest.raises(ValueError):
        Vers(source)


def test_invalid_input_type():
    with pytest.raises(TypeError):
        Vers(123)
