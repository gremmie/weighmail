import unittest
import collections

from weighmail.core import weighmail
from weighmail.utils import Label
from weighmail.observers import BaseObserver


class FakeClient(object):
    folder = None
    logout_called = False
    search_cnt = 0
    add_label_cnt = 0

    def __init__(self, labels, results, test_client):
        self.labels = labels
        self.results = results
        self.test_client = test_client

        self.searches = {}
        for label in labels:
            c = ''
            if label.min is not None:
                c = 'LARGER %d' % label.min
            if label.max is not None:
                if c:
                    c += ' '
                c += 'SMALLER %d' % label.max

            self.searches[c] = label

    def select_folder(self, folder):
        self.folder = folder

    def search(self, criteria):
        self.search_cnt += 1
        self.test_client.assertTrue(criteria in self.searches)
        return self.results[self.searches[criteria].name]

    def add_gmail_labels(self, msgs, labels):
        self.add_label_cnt += 1
        self.test_client.assertTrue(len(msgs) > 0)
        self.test_client.assertTrue(len(labels) == 1)
        self.test_client.assertTrue(labels[0] in self.results)
        self.test_client.assertTrue(msgs == self.results[labels[0]])

    def logout(self):
        self.logout_called = True


class TestObserver(BaseObserver):
    searches = collections.Counter()
    labels = []
    done_labels = []
    done = False

    def searching(self, label):
        self.searches[label] += 1

    def labeling(self, label, count):
        self.labels.append((label, count))

    def done_labeling(self, label, count):
        self.done_labels.append((label, count))

    def done(self):
        self.done = True


MB = 1024 * 1024
LABELS = [
    Label(name='big', min=2 * MB, max=5 * MB),
    Label(name='bigger', min=5 * MB, max=10 * MB),
    Label(name='huge', min=10 * MB, max=None)
]

RESULTS = {
    'big': [42, 1893, 2004],
    'bigger': [],
    'huge': [100, 200, 300, 400]
}


class WeighmailTestCase(unittest.TestCase):

    def test_simple(self):
        folder = '[Gmail]/All Mail'
        imap = FakeClient(LABELS, RESULTS, self)
        observer = TestObserver()

        weighmail(imap, folder, LABELS, observer)

        self.assertEqual(folder, imap.folder)
        self.assertEqual(3, imap.search_cnt)
        self.assertEqual(2, imap.add_label_cnt)
        self.assertFalse(imap.logout_called)
        
        self.assertEqual(observer.searches['big'], 1)
        self.assertEqual(observer.searches['bigger'], 1)
        self.assertEqual(observer.searches['huge'], 1)
        self.assertEqual(len(observer.searches), 3)

        self.assertEqual(len(observer.labels), 2)
        self.assertTrue(('big', 3) in observer.labels)
        self.assertTrue(('huge', 4) in observer.labels)

        self.assertEqual(len(observer.done_labels), 2)
        self.assertTrue(('big', 3) in observer.done_labels)
        self.assertTrue(('huge', 4) in observer.done_labels)

        self.assertTrue(observer.done)
