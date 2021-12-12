# TODO implement parameter change on action trigger

from typing import NamedTuple, List, Callable, Dict, Set, Tuple
from decimal import Decimal

def modify_args(modifier, ignored: Tuple[str] = tuple()):
    def decorator(named_tuple):
        def wrapper(*args, **kwargs):
            fields = named_tuple._fields
            mapper = lambda field, arg: arg if field in ignored else modifier(arg)

            modified_args = [
                    mapper(fields[i], arg)
                    for i, arg in enumerate(args)]
            modified_kwargs = {
                    field: mapper(field, arg)
                    for field, arg in kwargs.items()}

            return named_tuple(*modified_args, **modified_kwargs)

        return wrapper

    return decorator


class Number(Decimal):
    def __repr__(self):
        return str(self)


@modify_args(Number)
class Effect(NamedTuple):
    start_val_boost: Number
    min_val_boost: Number
    max_val_boost: Number
    delta_boost: Number


@modify_args(Number, ('affected_by',))
class ParameterConf(NamedTuple):
    start_val: Number
    min_val: Number
    max_val: Number
    delta: Number
    is_locked: bool = False
    affected_by: List[Effect] = []
    wait: Number = Number(0)

    def validate(self):
        if self.min_val > self.max_val:
            raise ValueError('min > max')
        if self.start_val < self.min_val:
            raise ValueError('start < min')
        if self.start_val > self.max_val:
            raise ValueError('start > max')


class Parameter:
    curr_val: Number
    min: Number
    max: Number
    delta: Number
    wait: Number

    def __init__(self, conf):
        conf.validate()
        self.curr_val = conf.start_val
        self.min = conf.min_val
        self.max = conf.max_val
        self.delta = conf.delta
        self.wait = conf.wait

    def next_action(self):
        if self.wait:
            self.wait -= 1
            return 
        self.set_value(self.curr_val + self.delta)

    def set_value(self, value: Number):
        if value < self.min:
            value = self.min
        elif value > self.max:
            value = self.max
        self.curr_val = value

    def apply_delta(self, delta: Number):
        self.set_value(self.curr_val + delta)

    def apply_effect(self, effect: Effect):
        self.curr_val += effect.start_val_boost
        self.min += effect.min_val_boost
        self.max += effect.max_val_boost
        self.delta += effect.delta_boost

    def __repr__(self):
        return f'[{self.curr_val}, {self.min}-{self.max}, {self.delta}, {self.wait}]'


class ParameterHolder(dict):
    class ParameterLock(NamedTuple):
        parameter: Parameter
        is_locked: bool = False

        def __repr__(self):
            locked = 'L' if self.is_locked else ''
            return str(self.parameter) + locked

        def locked(self, is_locked: bool):
            return type(self)(self.parameter, is_locked)

        def param(self, parameter: Parameter):
            return type(self)(parameter, self.is_locked)

    effects: Set[Effect]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.effects = set()

    def __setitem__(self, name: str, conf: ParameterConf):
        parameter = Parameter(conf)
        for effect in self.effects:
            if effect in conf.affected_by:
                parameter.apply_effect(effect)

        current = self.get(name)
        if current is not None:
            lock = current.param(parameter)
        else:
            lock = ParameterHolder.ParameterLock(parameter, conf.is_locked)
        super().__setitem__(name, lock)

    def change_param(self, name: str, value: Number):
        lock = self[name]
        lock.parameter.set_value(value)

    def apply_delta(self, name: str, delta: Number):
        lock = self[name]
        lock.parameter.apply_delta(delta)

    def add_effect(self, effect: Effect):
        self.effects.add(effect)

    def remove_effect(self, effect: Effect):
        self.effects.discard(effect)

    def next_action(self):
        for lock in self.values():
            if not lock.is_locked:
                lock.parameter.next_action()

    def set_locked(self, name: str, is_locked: bool):
        lock = self[name]
        super().__setitem__(name, lock.locked(is_locked))


class ConfigEntry(NamedTuple):
    pool_name: str
    config: ParameterConf
    add_effects: Set[Effect] = set()
    remove_effects: Set[Effect] = set()

