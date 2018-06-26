# NOTE: Requires fixtures/dict.pyi

from typing import Dict, Type, TypeVar, Optional, Any

_T = TypeVar('_T')


def Arg(type: _T = ..., name: Optional[str] = ...) -> _T: ...

def DefaultArg(type: _T = ..., name: Optional[str] = ...) -> _T: ...

def NamedArg(type: _T = ..., name: Optional[str] = ...) -> _T: ...

def DefaultNamedArg(type: _T = ..., name: Optional[str] = ...) -> _T: ...

def VarArg(type: _T = ...) -> _T: ...

def KwArg(type: _T = ...) -> _T: ...


def TypedDict(typename: str, fields: Dict[str, Type[_T]], *, total: Any = ...) -> Type[dict]: ...

# This is intended as a class decorator, but mypy rejects abstract classes
# when a Type[_T] is expected, so we can't give it the type we want
def trait(cls: Any) -> Any: ...

class NoReturn: pass
