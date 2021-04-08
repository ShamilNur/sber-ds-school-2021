from hw1.leetcode.valid_parentheses import is_valid


def test_on_empty_input():
    braces = ''
    assert is_valid(braces)


def test_on_a_single_type_of_parentheses():
    braces_list = ['[][]', '[[]]', '[[]]']

    for braces in braces_list:
        assert is_valid(braces)

    braces_list = ['[[][', '[][', '[', '][]]]', '[]]', '[][][]][]]']
    for braces in braces_list:
        assert not is_valid(braces)


def test_on_two_types_of_parentheses():
    braces_list = ['[][]{}{}', '[{}[{}]]', '[[{}]]{{}}', '{[{[]{}}]{}}']

    for braces in braces_list:
        assert is_valid(braces)

    braces_list = ['[][]{}[{}', '[[{}[{}]]', '[[{]}]]{{}}', '[]{}}']

    for braces in braces_list:
        assert not is_valid(braces)


def test_on_all_types_of_parentheses():
    braces_list = ['[()()()][()](){}{}', '[{}()[{}]()]', '(([[{}]]{{}}))', '{[{[()]{()}}]{}}']

    for braces in braces_list:
        assert is_valid(braces)

    braces_list = ['[()][(((]{}[{}', '[[{))}[{}]]', '[(([{]}]]{{}}', '({[]}']

    for braces in braces_list:
        assert not is_valid(braces)
