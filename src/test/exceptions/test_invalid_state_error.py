import pytest

from src.exceptions.invalid_state_error import InvalidStateError

ARG_0 = "3240- 3kfom3 ;m"
ARG_1 = "This is a english sentence."


class TestInvalidStateError:

    def test_exception_raise_no_args(self):
        with pytest.raises(InvalidStateError):
            raise InvalidStateError()

    def test_exception_raise_one_arg(self):
        try:
            raise InvalidStateError(ARG_0)
        except InvalidStateError as e:
            assert True
            a0 = e.args[0]
            assert a0 == ARG_0
        else:
            pytest.fail()

    def test_exception_raise_two_args(self):
        try:
            raise InvalidStateError(ARG_0, ARG_1)
        except InvalidStateError as e:
            assert True
            arg0 = e.args[0]
            arg1 = e.args[1]
            assert arg0 == ARG_0
            assert arg1 == ARG_1
        else:
            pytest.fail()
