"""Plugin to deduce types from the format strings used in the struct module."""
from typing import Union, List, Optional

from mypy.plugin import FunctionContext, MethodContext, MethodSigContext
from mypy.nodes import Expression, StrExpr, BytesExpr, UnicodeExpr, ARG_POS
from mypy.types import Type, CallableType, TupleType, Instance, LiteralType, NoneType, AnyType
import struct
import re

CHAR_TO_TYPE = {
    '?': 'builtins.bool',
    'e': 'builtins.float',
    'f': 'builtins.float',
    'd': 'builtins.float',
}
CHAR_TO_TYPE.update(dict.fromkeys('bBhHiIlLqQnNP', 'int'))


def _parse_format(
        ctx: Union[FunctionContext, MethodContext],
        fmt_type: Type,
        fmt: Expression,
) -> Optional[List[Type]]:
    """Given the expression for the format string, compute the types it specifies.

    If dynamic or unparsable, return None.
    """
    if isinstance(fmt, Instance) and fmt.last_known_value is not None:
        fmt = fmt.last_known_value

    if isinstance(fmt_type, LiteralType) and fmt_type.fallback.type.fullname() in (
            'builtins.bytes', 'builtins.str', 'builtins.unicode'):
        fmt_value = fmt_type.value
    elif isinstance(fmt, (BytesExpr, StrExpr, UnicodeExpr)):
        fmt_value = fmt.value
    else:
        return None  # Dynamic value

    try:
        struct.calcsize(fmt_value)
    except struct.error:
        ctx.api.fail('Invalid struct format ' + repr(fmt_value), ctx.context)
        return None

    # It should be a valid value now.
    output = []

    if ctx.api.options.python_version >= (3, ):
        bytes_type = ctx.api.named_generic_type('builtins.bytes', [])
    else:
        bytes_type = ctx.api.named_generic_type('builtins.str', [])

    for match in re.finditer('([0-9]*)([a-zA-Z?])', fmt_value.strip('<>=@!')):
        repeat_str, type_char = match.groups()

        if type_char == 'x':
            continue

        repeats = int(repeat_str) if repeat_str else 1

        if type_char in 'sp':
            # Strings, which only produce a single value regardless of repeat
            # count
            output.append(bytes_type)
            continue
        elif type_char == 'c':
            rep_type = bytes_type
        else:
            rep_type = ctx.api.named_generic_type(CHAR_TO_TYPE[type_char], [])

        output.extend([rep_type] * repeats)
    return output
FUNC_CALLBACKS = {
}

METH_CALLBACKS = {
}
