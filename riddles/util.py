def is_square(num: int) -> bool:
    if num < 0:
        return False
    if num == 0 or num == 1:
        return True
    x = num // 2
    seen = {x}
    while x * x != num:
        x = (x + (num // x)) // 2
        if x in seen:
            return False
        seen.add(x)
    return True
