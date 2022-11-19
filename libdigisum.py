def digisum(n: int = 0) -> int:
    return sum([int(i) for i in str(n)])


class Step:
    def __init__(self, add1: int, add2: int):
        self.add1 = add1
        self.add2 = add2
        self.dsum = digisum(add1 + add2)

    def to_string(self) -> str:
        return "取 {} + {} = {}, 加入 {}".format(
            self.add1, self.add2, self.add1 + self.add2, self.dsum
        )


def expected_answer(n: int) -> int:
    if n < 10:
        return n
    k = sum(range(1, n + 1))
    while k >= 10:
        k = digisum(k)
    numlen = len(str(n)) - 1
    maxget = int(str(n)[:1]) * (10**numlen) - 1
    if n - maxget == 10**numlen:
        maxget = n
    maxsum = digisum(maxget)
    while maxsum > 0:
        sumsum = digisum(maxsum)
        while sumsum >= 10:
            sumsum = digisum(sumsum)
        if sumsum == k:
            return maxsum
        maxsum -= 1

    return 1


def solve_min(n: int) -> dict:
    steps = []
    nums = list(range(1, n + 1))
    for i in range(n - 1, 1, -1):
        steps.append(Step(nums[i + 1], nums[i]))
        nums[i] = steps[-1].dsum
    steps.append(Step(nums[2], nums[1]))
    return {"answer": steps[-1].dsum, "steps": steps}


def sequential_merge(nums: list, l: int, r: int) -> list:
    steps = []
    for i in range(l + 1, r + 1):
        steps.append(Step(nums[i - 1], nums[i]))
        nums[i] = steps[-1].dsum
    return steps


def solve_max(n: int) -> dict:
    steps = []

    e = n
    k = 0
    while e > 0:
        k += 1
        e //= 10
    k -= 1
