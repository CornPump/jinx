# given an original int and destination int
# adds or subtracts digits to get destination's number of digits
def straighten_digits(orig: int, dest: int) -> int:
    diff = int(len(str(orig))) - dest
    # add zeros
    if diff < 0:
        orig = orig * pow(10, abs(diff))
    # subtract zeros
    elif diff > 0:
        orig = int(orig / (pow(10, diff)))
    return orig
