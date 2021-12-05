#TODO check if works with float
#TODO wrap with Decimal
#TODO manual parameter change
#TODO add parameter wait

from typing import NamedTuple, List, Callable, Dict, Set, Tuple

class Effect(NamedTuple):
    start_val_boost: int
    min_val_boost: int
    max_val_boost: int
    delta_boost: int

class ParameterConf(NamedTuple):
    start_val: int
    min_val: int
    max_val: int
    delta: int
    affected_by: List[Effect] = []

    def validate(self):
        if self.min_val > self.max_val:
            raise ValueError('min > max')
        if self.start_val < self.min_val:
            raise ValueError('start < min')
        if self.start_val > self.max_val:
            raise ValueError('start > max')


class Parameter:
    curr_val: int
    min: int
    max: int
    delta: int

    def __init__(self, conf):
        conf.validate()
        self.curr_val = conf.start_val
        self.min = conf.min_val
        self.max = conf.max_val
        self.delta = conf.delta_val

    def next_action(self):
        next_val = self.curr_val + self.conf.delta
        if next_val < self.conf.min_val:
            next_val = self.conf.min_val
        elif next_val > self.conf.max_val:
            next_val = self.conf.max_val
        self.curr_val = next_val

    def apply_effect(self, effect: Effect):
        curr_val += effect.start_val_boost
        min += effect.min_val_boost
        max += effect.max_val_boost
        delta += effect.delta_boost

    def __repr__(self):
        return f'[{self.curr_val}, {self.min}-{self.max}, {self.delta}]'


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
        if not isinstance(conf, ParameterConf):
            raise ValueError(f'{conf} is not a ParameterConf')

        parameter = Parameter(conf)
        for effect in self.effects:
            if effect in conf.affected_by:
                parameter.apply_effect(effect)

        current = self.get(name)
        if current is not None:
            lock = current.param(parameter)
        else:
            lock = ParameterHolder.ParameterLock(parameter)
        super().__setitem__(name, lock)

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


class HolderConfig(NamedTuple):
    holder: ParameterHolder
    parameters: Dict[str, Tuple[str, ParameterConf, List[Effect]]]

    def action(self, name: str):
        pool_name, conf, effects = parameters[name]
        holder[pool_name] = conf
        for effect in effects:
            holder.add_effect(effect)
