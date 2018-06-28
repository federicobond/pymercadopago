"""
Example test.

"""
from hamcrest import (
    assert_that,
    equal_to,
    is_,
)


def test_math():
    assert_that(1 + 1, is_(equal_to(2)))
