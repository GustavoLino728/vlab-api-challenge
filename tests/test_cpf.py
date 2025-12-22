from app.utils.cpf import is_valid_cpf, only_digits

VALID_CPF = "03890779093"
INVALID_CPF_1 = "12345678900"
INVALID_CPF_2 = "00000000000"
INVALID_CPF_3 = "11111111111"


def test_only_digits_removes_non_numeric():
    assert only_digits("038.907.790-93") == VALID_CPF


def test_is_valid_cpf_true_for_valid_number():
    assert is_valid_cpf(VALID_CPF) is True


def test_is_valid_cpf_false_for_invalid_number():
    assert is_valid_cpf(INVALID_CPF_1) is False
    assert is_valid_cpf(INVALID_CPF_2) is False
    assert is_valid_cpf(INVALID_CPF_3) is False