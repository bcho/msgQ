from msgQ.pub import publish

testcases = [
    ('*.*', 'foo.bar', True),
    ('foo.*', 'foo.bar', True),
    ('*.bar', 'foo.bar', True),
    ('foo.bar.baz', 'foo.bar', False),
    ('foo', 'foo.bar', True),
    ('foo.baz', 'foo.bar', False)
]


for msg, topic, _ in testcases:
    publish(msg, topic)
