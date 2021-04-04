def is_valid(s: str) -> bool:
    stack = []

    for i in range(len(s)):
        brace = s[i]
        if brace == '(' or brace == '[' or brace == '{':
            stack.append(brace)
        else:
            if len(stack) == 0:
                return False
            _open = stack.pop()
            if _open == '(' and brace != ')' or \
                    _open == '[' and brace != ']' or \
                    _open == '{' and brace != '}':
                return False

    return len(stack) == 0
