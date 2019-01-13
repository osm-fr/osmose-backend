"""A corrector for the 'opening_hours' fields from OpenStreetMap.

Provides a 'sanitize_field()' function, which tries to fix the most
current errors in the given field (takes and returns a string).

It can raise the following exceptions:

- TypeError : If the given field is not a string.
- SanitizeError : The generic exception of 'oh_sanitizer',
    raised when the field can't be parsed (if it is too complex, or invalid).
- InconsistentField : Inheriting from SanitizeError,
    raised when the field contains an invalid pattern which can't
    be corrected automatically.

Example:
>>> import oh_sanitizer
>>> print(oh_sanitizer.sanitize_field("mo-fr 10h - 7:00 pm"))
"Mo-Fr 10:00-19:00"
"""

__version__ = "0.1.9"
__appname__ = "oh_sanitizer"
__author__ = "rezemika <reze.mika@gmail.com>"
__licence__ = "AGPLv3"

from .main import sanitize_field, SanitizeError, InconsistentField
