"""Adaptation of the Python standard library JSONEncoder to encode `NaN` as 'null'
Compare to https://github.com/python/cpython/blob/3.9/Lib/json/encoder.py
The only functional difference is in the definition of `floatstr` where 'NaN', 'Infinity', and '-Infinity' are encoded as 'null'
"""
from json import JSONEncoder
from json.encoder import (
    _make_iterencode,
    py_encode_basestring,
    py_encode_basestring_ascii,
)

try:
    from _json import encode_basestring_ascii as c_encode_basestring_ascii
except ImportError:
    c_encode_basestring_ascii = None
try:
    from _json import encode_basestring as c_encode_basestring
except ImportError:
    c_encode_basestring = None
try:
    from _json import make_encoder as c_make_encoder
except ImportError:
    c_make_encoder = None

INFINITY = float("inf")
encode_basestring = c_encode_basestring or py_encode_basestring
encode_basestring_ascii = c_encode_basestring_ascii or py_encode_basestring_ascii


class IgnoreNanEncoder(JSONEncoder):
    def iterencode(self, o, _one_shot=False):
        """Encode the given object and yield each string
        representation as available.
        For example::
            for chunk in JSONEncoder().iterencode(bigobject):
                mysocket.write(chunk)
        """
        if self.check_circular:
            markers = {}
        else:
            markers = None
        if self.ensure_ascii:
            _encoder = encode_basestring_ascii
        else:
            _encoder = encode_basestring

        def floatstr(
            o, _repr=float.__repr__, _inf=INFINITY, _neginf=-INFINITY,
        ):
            if o != o or o == _inf or o == _neginf:
                return "null"
            else:
                return _repr(o)

        _iterencode = _make_iterencode(
            markers,
            self.default,
            _encoder,
            self.indent,
            floatstr,
            self.key_separator,
            self.item_separator,
            self.sort_keys,
            self.skipkeys,
            _one_shot,
        )
        return _iterencode(o, 0)
