import re


def only_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def is_valid_cpf(cpf: str) -> bool:
    cpf = only_digits(cpf)

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    nums = [int(d) for d in cpf]

    s1 = sum(nums[i] * (10 - i) for i in range(9))
    dv1 = (s1 * 10) % 11
    dv1 = 0 if dv1 == 10 else dv1

    s2 = sum(nums[i] * (11 - i) for i in range(10))
    dv2 = (s2 * 10) % 11
    dv2 = 0 if dv2 == 10 else dv2

    return nums[9] == dv1 and nums[10] == dv2
