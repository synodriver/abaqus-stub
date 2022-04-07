"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""
from types import FunctionType
from io import BytesIO
import sys

builtins = ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError',
            'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError',
            'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning',
            'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FileExistsError',
            'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError',
            'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError',
            'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError',
            'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented',
            'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError',
            'ProcessLookupError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError',
            'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning',
            'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError',
            'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError',
            'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError', '_',
            '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__',
            '__spec__', 'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes',
            'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict',
            'dir', 'divmod', 'enumerate', 'eval', 'exec', 'execfile', 'exit', 'filter', 'float', 'format',
            'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int',
            'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview',
            'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr',
            'reversed', 'round', 'runfile', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum',
            'super', 'tuple', 'type', 'vars', 'zip', 'xrange', 'unicode']


def ensure_bytes(data):
    if sys.version_info[0] == 3:
        return data.encode()
    else:
        return data


def dump_any(name, v, file, intendent):
    if getattr(v, "__name__", None) not in builtins:
        if type(v) == FunctionType:
            dump_function(v, file, intendent)
        elif type(v) == type:
            dump_class(v, file, intendent)
        elif isinstance(v, str):
            file.write(ensure_bytes("    " * intendent + name + " = \"" + str(v) + "\"\r\n"))
        elif isinstance(v, tuple):
            file.write(ensure_bytes("    " * intendent + name + " = " + str(tuple(v)) + "\r\n"))
        elif isinstance(v, int):
            file.write(ensure_bytes("    " * intendent + name + " = " + str(v) + "\r\n"))
        elif isinstance(v, dict):
            file.write(ensure_bytes("    " * intendent + name + " = " + str(v) + "\r\n"))


def dump_module(module, file):
    for k in dir(module):
        if k not in builtins:
            v = getattr(module, k)
            dump_any(k, v, file, 0)


def dump_function(func, file, intendent):
    file.write(ensure_bytes("    " * intendent + "def %s(" % func.__name__))
    doc = func.__doc__
    file.write(ensure_bytes("*args, **kwargs):\r\n"))
    file.write(
        ensure_bytes("    " * intendent + "    \"\"\"%s\"\"\"\r\n" % doc + "    " * intendent + "    pass\r\n\r\n"))


def dump_class(cls, file, intendent):
    file.write(ensure_bytes("    " * intendent + "class %s:\r\n" % cls.__name__))
    file.write(ensure_bytes("    " * (intendent + 1) + "\"\"\"%s\"\"\"\r\n" % cls.__doc__))
    for k in dir(cls):
        if k != "__doc__" and k != type and k != "__class__":
            v = getattr(cls, k, None)
            if v is not None:
                dump_any(k, v, file, intendent + 1)


if __name__ == "__main__":
    def test(a, b):
        """
        我是注释
        :param a:
        :param b:
        :return:
        """
        return a + b


    class TestClass:
        """我也是注释"""
        test = 1

        def __init__(self, a, b):
            """我是注释"""
            pass

        def gu(self, c):
            """我是一个方法"""
            pass


    f = BytesIO()
    dump_any("sasa",  TestClass,  f, 0)
    print(f.getvalue().decode())

    # import abaqus
    # import py2
    #
    # f = open("abaqus.pyi", "wb")
    # py2.dump_module(abaqus, f)
