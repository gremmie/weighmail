import unittest

from weighmail.utils import get_limit, make_label


TEST_DATA = [
    ('0', 0),
    ('42', 42),
    ('500623', 500623),
    ('1KB', 1024),
    ('2KB', 2048),
    ('1MB', 1024 * 1024),
    ('5MB', 5 * 1024 * 1024),
    ('1GB', 1024 * 1024 * 1024),
    ('10GB', 10 * 1024 * 1024 * 1024),
    ('0KB', 0),
    ('0MB', 0),
    ('0GB', 0),
]

INVALID_TEST_DATA = "foo -13 120JB $*)".split()


class GetLimitTestCase(unittest.TestCase):

    def test_get_limit(self):

        for x in TEST_DATA:
            self.assertEqual(get_limit(x[0]), x[1])

    def test_get_limit_lower(self):

        for x in TEST_DATA:
            self.assertEqual(get_limit(x[0].lower()), x[1])

    def test_get_limit_mixed(self):

        for x in TEST_DATA:
            if x[0].endswith('B'):
                x1 = x[0][:-2] + x[0][-2].lower() + x[0][-1] 
                x2 = x[0][:-2] + x[0][-2] + x[0][-1].lower()
                self.assertEqual(get_limit(x1), x[1])
                self.assertEqual(get_limit(x2), x[1])

    def test_invalid(self):

        for x in INVALID_TEST_DATA:
            self.assertRaises(ValueError, get_limit, x)

    def test_none(self):

        self.assertIsNone(get_limit(''))
        self.assertIsNone(get_limit(None))


class MakeLabelTestCase(unittest.TestCase):

    def test_simple(self):

        label = make_label('red', '50', '100')
        self.assertEqual(label.name, 'red')
        self.assertEqual(label.min, 50)
        self.assertEqual(label.max, 100)

    def test_no_min(self):

        for v in ['', None]:
            label = make_label('red', v, '100')
            self.assertEqual(label.name, 'red')
            self.assertIsNone(label.min)
            self.assertEqual(label.max, 100)

    def test_no_max(self):

        for v in ['', None]:
            label = make_label('red', '210', v)
            self.assertEqual(label.name, 'red')
            self.assertEqual(label.min, 210)
            self.assertIsNone(label.max)

    def test_invalid(self):

        self.assertRaises(ValueError, make_label, 'red', None, None)
        self.assertRaises(ValueError, make_label, 'red', '', None)
        self.assertRaises(ValueError, make_label, 'red', None, '')
        self.assertRaises(ValueError, make_label, 'red', '', '')
        self.assertRaises(ValueError, make_label, 'red', '100', '90')
