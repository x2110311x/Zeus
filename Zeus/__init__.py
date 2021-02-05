import sys
import inspect
import logging

from textwrap import dedent

class InitClass:
    def find_module(self, fullname, path=None):
        if fullname == 'requests':
            return self
        return None

    def _get_import_chain(self, *, until=None):
        stack = inspect.stack()[2:]
        try:
            for frameinfo in stack:
                try:
                    if not frameinfo.code_context:
                        continue

                    data = dedent(''.join(frameinfo.code_context))
                    if data.strip() == until:
                        raise StopIteration

                    yield frameinfo.filename, frameinfo.lineno, data.strip()
                    del data
                finally:
                    del frameinfo
        finally:
            del stack

    def _format_import_chain(self, chain, *, message=None):
        lines = []
        for line in chain:
            lines.append("In %s, line %s:\n    %s" % line)

        if message:
            lines.append(message)

        return '\n'.join(lines)

    def load_module(self, name):
        import_chain = tuple(self._get_import_chain(until='from .bot import MusicBot'))
        import_tb = self._format_import_chain(import_chain)

__all__ = ['Zeus']

_func_prototype = "def {logger_func_name}(self, message, *args, **kwargs):\n" \
                  "    if self.isEnabledFor({levelname}):\n" \
                  "        self._log({levelname}, message, args, **kwargs)"

def _add_logger_level(levelname, level, *, func_name = None):
    """

    :type levelname: str
        The reference name of the level, e.g. DEBUG, WARNING, etc
    :type level: int
        Numeric logging level
    :type func_name: str
        The name of the logger function to log to a level, e.g. "info" for log.info(...)
    """

    func_name = func_name or levelname.lower()

    setattr(logging, levelname, level)
    logging.addLevelName(level, levelname)

    exec(_func_prototype.format(logger_func_name=func_name, levelname=levelname), logging.__dict__, locals())
    setattr(logging.Logger, func_name, eval(func_name))


_add_logger_level('EVERYTHING', 1)
_add_logger_level('ExternalAPI', 4)

log = logging.getLogger(__name__)
log.setLevel(logging.EVERYTHING)

fhandler = logging.FileHandler(filename='logs/Zeus.log', encoding='utf-8', mode='a+')
fhandler.setFormatter(logging.Formatter(
    "[{relativeCreated:.16f}] {asctime} - {levelname} - {name} | "
    "In {filename}::{threadName}({thread}), line {lineno} in {funcName}: {message}",
    style='{'
))
log.addHandler(fhandler)

del _func_prototype
del _add_logger_level
del fhandler