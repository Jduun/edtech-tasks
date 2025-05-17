import pytest

from solution1 import strict


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


@strict
def func_with_all_types(a: bool, b: str, c: float) -> int:
    return 10


@strict
def func_with_incorrect_return_type(a: int) -> bool:
    return "some string"


@strict
def func_with_unspecified_types(a, b: int) -> int:
    return 20


def test_correct_args_types():
    assert sum_two(2, 3) == 5
    assert func_with_all_types(True, "string", 1.2)
    assert func_with_unspecified_types("", 2)
    assert func_with_unspecified_types(True, 4)


def test_correct_kwargs_types():
    assert sum_two(a=5, b=7) == 12
    assert sum_two(b=10, a=-2) == 8
    assert func_with_all_types(a=False, b="", c=4.5)
    assert func_with_unspecified_types(a=3.5, b=10)


def test_correct_mixed_args_types():
    assert sum_two(30, b=12) == 42
    assert func_with_all_types(True, b="abcdef", c=1.5)
    assert func_with_unspecified_types("some string", b=20)


def test_incorrect_args_types():
    with pytest.raises(TypeError):
        sum_two(1, 2.4)
    with pytest.raises(TypeError):
        func_with_all_types(10, "", 3.4)


def test_incorrect_kwargs_types():
    with pytest.raises(TypeError):
        sum_two(a=2, b=5.4)
    with pytest.raises(TypeError):
        func_with_all_types(a=True, b=10, c=3.4)


def test_incorrect_mixed_args_types():
    with pytest.raises(TypeError):
        sum_two(2, b=4.4)
    with pytest.raises(TypeError):
        func_with_all_types(True, b=20, c=4.4)


def test_incorrect_return_type():
    with pytest.raises(TypeError):
        func_with_incorrect_return_type(20)
