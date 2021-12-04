from typing import NamedTuple, List, Callable
import inspect

class ParameterConf(NamedTuple):
    start_val: int
    min_val: int
    max_val: int
    delta_func: Callable[[int], int]
    
    def validate(self):
        if self.min_val > self.max_val:
            raise ValueError('min > max')
        if self.start_val < self.min_val:
            raise ValueError('start < min')
        if self.start_val > self.max_val:
            raise ValueError('start > max')


class Parameter:
    value: int
    conf: ParameterConf

    def __init__(self, conf):
        conf.validate()
        self.curr_val = conf.start_val
        self.conf = conf

    @property
    def min(self):
        return self.conf.min_val

    @property
    def max(self):
        return self.conf.max_val

    @property
    def value(self):
        return self.curr_val

    def next_action(self):
        next_val = self.conf.delta_func(self.curr_val)
        if next_val < self.conf.min_val:
            next_val = self.conf.min_val
        elif next_val > self.conf.max_val:
            next_val = self.conf.max_val
        self.curr_val = next_val

    def __str__(self):
        delta_code = inspect.getsource(self.conf.delta_func) \
                .remove_prefix('eval(') \
                .remove_suffix(')')
        return f'[{self.value}, {self.min}-{self.max}, {delta_code}]'

    def __repr__(self):
        return self.__str__()


class ParameterHolder(dict):
    def __setitem__(self, name: str, parameter: Parameter):
        if not isinstance(parameter, Parameter):
            raise ValueError(f'{parameter} is not a Parameter')
        super().__setitem__(name, parameter)

    def next_action(self):
        for parameter in self:
            parameter.next_action()

