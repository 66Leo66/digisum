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
    # k = sum(range(1, n + 1))
    k = (n + 1) * n / 2
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
    nums = list(range(0, n + 1))
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


def solve_max(n: int, exp_ans: int) -> dict:
    steps = []
    nums = list(range(0, n + 1))

    k = len(str(n)) - 1

    mid = 0
    if k != 0:
        avg = exp_ans // k
        if exp_ans % k != 0:
            avg += 1
        if avg >= 9:
            avg = 8
        mid = int(str(avg) * (k - 1)) * 10
        if exp_ans - (k - 1) * avg >= 9:
            mid += 8
        else:
            mid += exp_ans - (k - 1) * avg
    else:
        mid = exp_ans

    steps.extend(sequential_merge(nums, 1, mid - 1))
    steps.extend(sequential_merge(nums, mid + 1, n))

    if 1 < mid and mid < n:
        steps.append(Step(nums[mid - 1], nums[n]))
        steps.append(Step(steps[-1].dsum, mid))
    else:
        op = nums[n] if mid == 1 else nums[n - 1]
        steps.append(Step(op, mid))

    return {"answer": steps[-1].dsum, "steps": steps}
