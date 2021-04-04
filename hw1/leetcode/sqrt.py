def my_sqrt(x: int) -> int:
        if x == 0 or x == 1:
            return x

        left, right = 0, x
        while left <= right:
            mid = left + (right - left) // 2
            sqrt = x // mid

            if sqrt == mid:
                return sqrt
            elif sqrt < mid:
                right = mid - 1
            else:
                left = mid + 1

        return right
