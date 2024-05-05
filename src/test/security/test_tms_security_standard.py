from src.security.security import TMSSecurityStandard


def sec():
    return TMSSecurityStandard()


def test_hash_1():
    assert sec().hash("234090dl3OD-") == sec().hash("234090dl3OD-")


def test_hash_2():
    assert sec().hash("aspw)#kd-LEW-") == sec().hash("aspw)#kd-LEW-")


def test_hash_3():
    assert sec().hash("l3kd0c-3kl2ls-i2omx0") == TMSSecurityStandard().hash("l3kd0c-3kl2ls-i2omx0")


def test_hash_4():
    try:
        sec().hash(None)
        assert False
    except TypeError:
        assert True


def test_hash_5():
    try:
        sec().hash(01.3)
        assert False
    except TypeError:
        assert True


def test_create_auth_token_1():
    # this technically might on rare occasion fail.
    assert sec().create_auth_token() != sec().create_auth_token()


def test_create_auth_token_2():
    # this technically might on rare occasion fail.
    assert TMSSecurityStandard().create_auth_token() != TMSSecurityStandard().create_auth_token()


def test_is_password_valid_length_1():
    assert not sec().is_password_valid_length("1234567a_AB")


def test_is_password_valid_length_2():
    assert sec().is_password_valid_length("12345r4367a_AB")


def test_is_password_valid_length_3():
    assert not sec().is_password_valid_length("short")


def test_is_password_valid_length_4():
    assert sec().is_password_valid_length("                ")


def test_password_has_number_1():
    assert not sec().password_has_number("alllowercasebutlong")


def test_password_has_number_2():
    assert sec().password_has_number("alllowercaseb7utlong")


def test_password_has_lowercase_1():
    assert not sec().password_has_lowercase("DKLD)@K#@LS")


def test_password_has_lowercase_2():
    assert sec().password_has_lowercase("alllowercaseb7utlong")


def test_password_has_uppercase_1():
    assert not sec().password_has_uppercase("_)#@+_adl5t7eo,f")


def test_password_has_uppercase_2():
    assert sec().password_has_uppercase("D")


def test_password_has_symbol_1():
    assert not sec().password_has_symbol("alphaNumeric90")


def test_password_has_symbol_2():
    assert sec().password_has_symbol("mostlyAlphaButAlitteNumeric908AndASymbol_")


def test_is_password_valid_1():
    assert sec().is_password_valid("Password123_")


def test_is_password_valid_2():
    assert sec().is_password_valid("LSKD)#-SDa+_kd93")


def test_is_password_valid_3():
    assert not sec().is_password_valid("")


def test_is_password_valid_4():
    assert not sec().is_password_valid("             ")


def test_is_password_valid_5():
    assert not sec().is_password_valid("LSKeokf0934j")


def test_is_password_valid_6():
    assert not sec().is_password_valid("L230d_)24")


def test_is_password_valid_7():
    try:
        sec().is_password_valid(None)
        assert False
    except TypeError:
        assert True


def test_is_password_valid_8():
    try:
        sec().is_password_valid(90)
        assert False
    except TypeError:
        assert True
