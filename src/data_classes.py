from collections import namedtuple

Dictionary_Entry = namedtuple('Dictionary_Entry', ['from_lang', 'to_lang', 'key', 'value', 'example'],
                              defaults=(None, None, None, None, None))
