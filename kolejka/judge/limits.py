# vim:ts=4:sts=4:sw=4:expandtab
import datetime

from kolejka.judge import config
from kolejka.judge.parse import *
from kolejka.judge.typing import *


__all__ = [ 'Limits', 'get_limits', ]
def __dir__():
    return __all__


class Limits(AbstractLimits):

    def __init__(self, cpu_time=None, real_time=None, memory=None, cores=None, pids=None):
        self._cpu_time = None
        self.set_cpu_time(cpu_time)
        self._real_time = None
        self.set_real_time(real_time)
        self._memory = None
        self.set_memory(memory)
        self._cores = None
        self.set_cores(cores)
        self._pids = None
        self.set_pids(pids)

    def __repr__(self):
        repr_dict = dict()
        for k,v in self.__dict__.items():
            if k in [ '_system', '_name' ]:
                continue
            if len(k) and k[0] == '_':
                k=k[1:]
            repr_dict[k] = repr(v)
        rep = f'{self.__class__.__name__}: {repr_dict}'
        return rep

    @property
    def cpu_time(self) -> datetime.timedelta:
        return self.get_cpu_time()
    def get_cpu_time(self):
        return self._cpu_time
    def set_cpu_time(self, cpu_time):
        self._cpu_time = None if cpu_time is None else parse_time(cpu_time)
    def update_cpu_time(self, cpu_time):
        if self.cpu_time is None:
            self.set_cpu_time(cpu_time)
        elif cpu_time is not None:
            self._cpu_time = min(self._cpu_time, parse_time(cpu_time))

    @property
    def real_time(self) -> datetime.timedelta:
        return self.get_real_time()
    def get_real_time(self):
        return self._real_time
    def set_real_time(self, real_time):
        self._real_time = None if real_time is None else parse_time(real_time)
    def update_real_time(self, real_time):
        if self.real_time is None:
            self.set_real_time(real_time)
        elif real_time is not None:
            self._real_time = min(self._real_time, parse_time(real_time))

    @property
    def memory(self) -> int:
        return self.get_memory()
    def get_memory(self):
        return self._memory
    def set_memory(self, memory):
        self._memory = None if memory is None else parse_memory(memory)
    def update_memory(self, memory):
        if self.memory is None:
            self.set_memory(memory)
        elif memory is not None:
            self._memory = min(self._memory, parse_memory(memory))

    @property
    def cores(self) -> int:
        return self.get_cores()
    def get_cores(self):
        return self._cores
    def set_cores(self, cores):
        self._cores = None if cores is None else int(cores)
    def update_cores(self, cores):
        if self.cores is None:
            self.set_cores(cores)
        elif cores is not None:
            self._cores = min(self._cores, int(cores))

    @property
    def pids(self) -> int:
        return self.get_pids()
    def get_pids(self):
        return self._pids
    def set_pids(self, pids):
        self._pids = None if pids is None else int(pids)
    def update_pids(self, pids):
        if self.pids is None:
            self.set_pids(pids)
        elif pids is not None:
            self._pids = min(self._pids, int(pids))


def get_limits(*args, **kwargs):
    if len(args) == 1 and isinstance(args[0], Limits):
        return args[0]
    if len(args) == 1 and isinstance(args[0], dict):
        args[0].update(kwargs)
        return Limits(**args[0])
    if len(args) != 0:
        raise ValueError
    return Limits(**kwargs)
