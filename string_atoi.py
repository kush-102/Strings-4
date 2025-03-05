class Solution:
    def myAtoi(self, s: str) -> int:
        s = s.strip()
        if len(s) == 0:
            return 0

        result = 0
        flag = True
        start_index = 0
        limit = 2**31
        lower_limit = -(2**31)

        if s[0] == "+":
            flag = True
            start_index = 1
        elif s[0] == "-":
            flag = False
            start_index = 1

        for i in range(start_index, len(s)):

            c = s[i]

            if c.isdigit():
                digit = int(c)
                result = result * 10 + digit

            else:
                break
        if not flag:
            result = -result

        if result >= limit:
            return limit - 1
        elif result <= lower_limit:
            return lower_limit
        else:
            return result

    # time complexity is O(n)
    # space complexity is O(1)
