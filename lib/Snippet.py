import unittest
import difflib
import re


WORDCHAR = re.compile(r'\w')
NO_CHANGE = ' '
ADD_CHANGE = '+'
SUB_CHANGE = '-'


def diff(a, b):
    parts = []
    currentBlock = []
    currentWord = ''
    currentDiff = ''
    inSub = False

    for i, s in enumerate(difflib.ndiff(a, b)):
        diffOp = s[0]
        char = s[2]

        if diffOp == NO_CHANGE:
            inSub = False

            if WORDCHAR.match(char) is None:
                if len(currentDiff) > 0:
                    currentBlock += [[currentDiff]]
                    currentDiff = ''

                if len(currentWord) > 0:
                    if len(currentBlock) > 0:
                        currentBlock += [currentWord]
                    else:
                        parts += [currentWord]

                    currentWord = ''

                if len(currentBlock) > 0:
                    if len(currentBlock) == 1:
                        parts += currentBlock
                    else:
                        parts += [currentBlock]
                    currentBlock = []
                    currentWord = ''

                parts += char

            else:
                currentWord += char

            hasDiff = False

        elif diffOp == ADD_CHANGE:
            if inSub and len(currentBlock) > 0 \
                    and len(currentBlock[len(currentBlock)-1]) == 0:
                currentBlock.pop()

            inSub = False

            if len(currentWord) > 0:
                currentBlock += [currentWord]
                currentWord = ''
            currentDiff += char

        elif diffOp == SUB_CHANGE:
            if inSub is False:
                if len(currentWord) > 0:
                    currentBlock += [currentWord]
                    currentWord = ''
                currentBlock += [[]]
                inSub = True

    if len(currentDiff) > 0:
        if len(currentBlock) > 0:
            currentBlock += [[currentDiff]]
        else:
            currentBlock = [currentDiff]
        currentDiff = ''

    if len(currentBlock) > 0:
        parts += [currentBlock]
    elif len(currentWord) > 0:
        parts += [currentWord]

    return parts


def diffToSnippet(d):
    snippet = ''
    position = 0

    for v in d:
        if type(v) == list:
            position += 1

            snippet += '${%i:' % position

            for v2 in v:
                if type(v2) == list:
                    position += 1

                    if len(v2) > 0:
                        snippet += '${%i:%s}' % (position, v2[0])
                    else:
                        snippet += '${%i}' % position
                else:
                    snippet += v2

            snippet += '}'
        else:
            snippet += v

    return snippet


def generate(a, b):
    return diffToSnippet(diff(a, b))


class GenerateTest(unittest.TestCase):
    def test_simple_trailing(self):
        a = 'Aaa Bbb'
        b = 'Aaa Ccc'
        e = 'Aaa ${1:Ccc}'

        self.assertEqual(generate(a, b), e)

    def test_simple_leading(self):
        a = 'Aaa Bbb'
        b = 'Ccc Bbb'
        e = "${1:Ccc} Bbb"

        self.assertEqual(generate(a, b), e)

    def test_simple_middle(self):
        a = 'Aaa Bbb Ccc'
        b = 'Aaa Ddd Ccc'
        e = 'Aaa ${1:Ddd} Ccc'

        self.assertEqual(generate(a, b), e)

    def test_nested(self):
        a = 'Mr. Jane Smith'
        b = 'Mr. Jack Smith'
        e = 'Mr. ${1:Ja${2:ck}} Smith'

        self.assertEqual(diffToSnippet(diff(a, b)), e)

    def test_fail_1(self):
        a = 'self.assertEqual()'
        b = 'self.assertNotEqual()'
        e = 'self.${1:assert${2:Not}Equal}()'

        self.assertEqual(diffToSnippet(diff(a, b)), e)

    def test_fail_2(self):
        a = 'self.assertNotEqual()'
        b = 'self.assertEqual()'
        e = 'self.${1:assert${2}Equal}()'

        self.assertEqual(diffToSnippet(diff(a, b)), e)

    def test_fail_3(self):
        a = 'Jane Doe'
        b = 'Sally Doe'
        e = '${1:S${2:ally}} Doe'

        self.assertEqual(diffToSnippet(diff(a, b)), e)


if __name__ == '__main__':
    unittest.main()
