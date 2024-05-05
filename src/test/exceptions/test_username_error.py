from src.exceptions.exceptions import UsernameError

ARG_0 = "message"
ARG_1 = "9023l"


def test_exception_raise_no_args():
    try:
        raise UsernameError()
    except UsernameError as e:
        assert True
    else:
        assert False


def test_exception_raise_one_arg():
    try:
        raise UsernameError(ARG_0)
    except UsernameError as e:
        assert True
        a0 = e.args[0]
        assert a0 == ARG_0
    else:
        assert False


def test_exception_raise_two_args():
    try:
        raise UsernameError(ARG_0, ARG_1)
    except UsernameError as e:
        assert True
        arg0 = e.args[0]
        arg1 = e.args[1]
        assert arg0 == ARG_0
        assert arg1 == ARG_1
    else:
        assert False
