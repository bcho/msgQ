import unittest

from msgQ.commands import _topic_cmp as topic_cmp


testcases = [
    ('*.*', 'foo.bar', True),
    ('foo.*', 'foo.bar', True),
    ('*.bar', 'foo.bar', True),
    ('foo.bar.baz', 'foo.bar', False),
    ('foo', 'foo.bar', True),
    ('foo.baz', 'foo.bar', False)
]


class TopicCMPText(unittest.TestCase):
    def test(self):
        for key, topic, result in testcases:
            print key, topic
            self.assertEqual(topic_cmp(key, topic), result)
