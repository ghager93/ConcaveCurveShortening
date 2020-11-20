from bin.util.base_dir import base_dir

CRITERIA_NOT_MET = 0
FIRST_ITERATION = 1
SECOND_ITERATION = 2
UPPER_LIMIT = 256

FILENAME = base_dir + 'lib/lookup/zhan_suen_neighbour_lookup.py'

def build_criteria_dict():
    criteria_dict = dict()
    for n in range(UPPER_LIMIT):
        criteria_dict[n] = _assign_criteria_score(n)

    return criteria_dict


def _assign_criteria_score(n: int):
    if not _criteria_a(n) or not _criteria_b(n):
        return CRITERIA_NOT_MET
    if _criteria_c(n) and _criteria_d(n):
        return FIRST_ITERATION
    if _criteria_c_dash(n) and _criteria_d_dash(n):
        return SECOND_ITERATION

    return CRITERIA_NOT_MET


def _criteria_a(n: int):
    return 2 <= _number_of_bits_high(n) <= 6


def _criteria_b(n: int):
    return _number_of_01_patterns_in_ordered_neighbours_set(n) == 1


def _criteria_c(n: int):
    return 0b00010101 & n != 0b00010101


def _criteria_d(n: int):
    return 0b01010100 & n != 0b01010100


def _criteria_c_dash(n: int):
    return 0b01000101 & n != 0b01000101


def _criteria_d_dash(n: int):
    return 0b01010001 & n != 0b01010001


def _number_of_bits_high(n: int):
    return bin(n).count('1')


def _number_of_01_patterns_in_ordered_neighbours_set(n: int):
    mask = 0b11000000
    pattern = 0b01000000
    cnt = 0
    for i in range(7):
        if mask & n == pattern:
            cnt += 1
        mask >>= 1
        pattern >>= 1

    if 0b10000001 & n == 0b10000000:
        cnt += 1

    return cnt


if __name__ == '__main__':
    pass
    # with open(FILENAME, 'w') as f:
    #     print(str(build_criteria_dict()), file=f)
